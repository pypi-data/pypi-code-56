import math, os
import numpy as np
import numpy.random as nr
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox 
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

#=================================
# パラメータ
#=================================
#figsize
FIGSIZE = 12

#コース生成
SCALE       = 10        # 固定
TRACK_RAD   = 400/SCALE  # 全長、260でkmくらい
TRACK_DETAIL_STEP = 30/SCALE #パネルの長さ
TRACK_TURN_RATE = 0.41 #曲率
TRACK_WIDTH = 50/SCALE #パネルの幅
BACK_COLOR = 'palegreen'#'lightcyan'
ROAD_COLOR = np.array([(0.8, 0.8, 0.8),
                       (0.75, 0.75, 0.75)])
#ROAD_COLOR = np.array(['paleturquoise',
#                       'skyblue'])

#シミュレーション
FPS         = 30



#=================================
# 関数
#=================================
#画像に車を乗せる
def plot_car(x, y, rad, img, zoom=1): 
    ax = plt.gca() 
    img_rotate = img.rotate(math.degrees(rad), expand=True)
    imo = OffsetImage(img_rotate, zoom=zoom)
    ab = AnnotationBbox(imo, (x, y), xycoords='data', frameon=False) 
    ax.add_artist(ab)
    #ax.update_datalim(np.column_stack([x, y])) 
    #ax.autoscale() 
    #return artists 


#=================================
# クラス
#=================================
class vcracing():
    def __init__(self, track_seed=None, verbose=0, car='BT46', track_len=400):
        if type(track_seed) is int:
            self.track_seed = track_seed
        else:
            self.track_seed = nr.randint(10000)
        nr.seed(self.track_seed)
        self.verbose = verbose
        
        #画像読み込み
        if car == 'avro':
            self.carimg = Image.open('top_avro.png').convert('RGBA'); self.carimg.close
        elif car == 'BT46':
            self.carimg = Image.open('top_BT46.png').convert('RGBA'); self.carimg.close
        elif car == 'P34':
            self.carimg = Image.open('top_P34.png').convert('RGBA'); self.carimg.close
        elif car == 'novgorod':
            self.carimg = Image.open('top_novgorod.png').convert('RGBA'); self.carimg.close
        elif car == 'twinturbo':
            self.carimg = Image.open('top_twinturbo.png').convert('RGBA'); self.carimg.close
        else:
            self.carimg = Image.open('top_BT46.png').convert('RGBA'); self.carimg.close
        
        self.track_len = track_len
        self.TRACK_RAD = (self.track_len/SCALE)**0.75 * 3.7
        
        #コース生成
        self.road = []
        self.road_color = []
        while True:
            success = self.make_course()
            if success:
                break
        #シード解除
        nr.seed(None)
        
        #グラフの範囲を取得
        self.road_max = [0, 0]
        self.road_min = [0, 0]
        self.road_max[0] = np.max(self.road[:, :, 0])
        self.road_max[1] = np.max(self.road[:, :, 1])
        self.road_min[0] = np.min(self.road[:, :, 0])
        self.road_min[1] = np.min(self.road[:, :, 1])
        self.road_max[0] *= 9/8
        self.road_max[1] *= 9/8
        self.road_min[0] *= 9/8
        self.road_min[1] *= 9/8
        #print(self.road_max, self.road_min)
        
        #全長の計算
        centers = np.array([np.mean(self.road[:, :, 0], axis=1), np.mean(self.road[:, :, 1], axis=1)])
        self.road_len = np.sum( ((centers[0, 1:] - centers[0, :-1])**2 + (centers[1, 1:] - centers[1, :-1])**2)**0.5 )
        #print(self.road_len)
        
        
        #reset        
        self.state = self.reset()
        
        text1 = '[Steer, Accel] where Steer in [-1, +1], Accel in [-1, +1]\n'
        text1 += 'Note Steer=-1 turns LEFT, Accel=-1 reverse gear.'
        self.action_space = text1
        text2 = 'dictionary of {\'pos\', \'velocity\', \'radian\', \'road\', \'visited\'}\n'
        text2 += 'np.shape(pos)=(2) of [x, y]\n'
        text2 += 'np.shape(velocity)=(1)\n'
        text2 += 'np.shape(rad)=(1) in [0, 2pi]\n'
        text2 += 'np.shape(raad)=(num_road, 4, 2) where 4 are corner poss of road panel.\n'
        text2 += 'np.shape(visited)=(1) in bool\n'
        self.observation_space = text2
        
        
    def reset(self):
        #報酬
        self.reward = 0.0
        self.reward_sum = 0.0
        #self.prev_reward = 0.0
        #時間
        self.t = 0.0
        self.frame = 0
        
        #グラフが呼ばれたか
        #self.firstrender = False
        
        #車
        self.pos = np.mean(self.road[0], axis=0)
        self.vel = [0, 0]
        
        self.rad = math.atan2(np.mean(self.road[0,:,0]) - np.mean(self.road[1,:,0]),
                              np.mean(self.road[1,:,1]) - np.mean(self.road[0,:,1]))
        self.rad_v = 0
        self.speed = 0
        
        self.visited = np.zeros(len(self.road), dtype=bool)
        self.visited_count = 0
        

        
        #返り値の準備
        info = {}
        info['position'] = self.pos
        info['velocity'] = self.vel
        info['radian'] = self.rad
        info['radian_v'] = self.rad
        info['road'] = self.road
        info['visited'] = self.visited
        info['visited_count'] = self.visited_count
        info['time'] = self.t
        info['frame'] = self.frame
        info['rewards'] = self.reward_sum
        info['actual_length'] = self.road_len
        info['speed'] = self.speed
        info['road_max'] = self.road_max
        info['road_min'] = self.road_min
        self.state = info
        return self.state

    def make_course(self):
        TRACK_RAD = self.TRACK_RAD
        CHECKPOINTS = int(3 * self.TRACK_RAD / 10)
        #print(CHECKPOINTS)
        
        # Create checkpoints
        checkpoints = []
        for c in range(CHECKPOINTS):
            alpha = 2*math.pi*c/CHECKPOINTS + nr.uniform(0, 2*math.pi*1/CHECKPOINTS)
            rad = nr.uniform(TRACK_RAD/3, TRACK_RAD)
            if c==0:
                alpha = 0
                rad = 1.5*TRACK_RAD
            if c==CHECKPOINTS-1:
                alpha = 2*math.pi*c/CHECKPOINTS
                self.start_alpha = 2*math.pi*(-0.5)/CHECKPOINTS
                rad = 1.5*TRACK_RAD
            checkpoints.append( (alpha, rad*math.cos(alpha), rad*math.sin(alpha)) )        

        # Go from one checkpoint to another to create track
        x, y, beta = 1.5*TRACK_RAD, 0, 0
        dest_i = 0
        laps = 0
        track = []
        no_freeze = 2500
        visited_other_side = False
        while 1:
            alpha = math.atan2(y, x)
            if visited_other_side and alpha > 0:
                laps += 1
                visited_other_side = False
            if alpha < 0:
                visited_other_side = True
                alpha += 2*math.pi
            while True: # Find destination from checkpoints
                failed = True
                while True:
                    dest_alpha, dest_x, dest_y = checkpoints[dest_i % len(checkpoints)]
                    if alpha <= dest_alpha:
                        failed = False
                        break
                    dest_i += 1
                    if dest_i % len(checkpoints) == 0: break
                if not failed: break
                alpha -= 2*math.pi
                continue
            r1x = math.cos(beta)
            r1y = math.sin(beta)
            p1x = -r1y
            p1y = r1x
            dest_dx = dest_x - x  # vector towards destination
            dest_dy = dest_y - y
            proj = r1x*dest_dx + r1y*dest_dy  # destination vector projected on rad
            while beta - alpha >  1.5*math.pi: beta -= 2*math.pi
            while beta - alpha < -1.5*math.pi: beta += 2*math.pi
            prev_beta = beta
            proj *= SCALE
            if proj >  0.3: beta -= min(TRACK_TURN_RATE, abs(0.001*proj))
            if proj < -0.3: beta += min(TRACK_TURN_RATE, abs(0.001*proj))
            x += p1x*TRACK_DETAIL_STEP
            y += p1y*TRACK_DETAIL_STEP
            track.append( (alpha,prev_beta*0.5 + beta*0.5,x,y) )
            if laps > 4: break
            no_freeze -= 1
            if no_freeze==0: break
        #print "\n".join([str(t) for t in enumerate(track)])

        # Find closed loop range i1..i2, first loop should be ignored, second is OK
        i1, i2 = -1, -1
        i = len(track)
        while True:
            i -= 1
            if i==0: return False  # Failed
            pass_through_start = track[i][0] > self.start_alpha and track[i-1][0] <= self.start_alpha
            if pass_through_start and i2==-1:
                i2 = i
            elif pass_through_start and i1==-1:
                i1 = i
                break

        assert i1!=-1
        assert i2!=-1

        track = track[i1:i2-0]
        
        #縦ズレを抑える
        sg_len = ((track[0][2] - track[-1][2])**2 + (track[0][3] - track[-1][3])**2)**0.5
        if sg_len > TRACK_DETAIL_STEP*1.25 or sg_len < TRACK_DETAIL_STEP*0.75:
            #print('false')
            #print('-', end='')
            return False

        first_beta = track[0][1]
        first_perp_x = math.cos(first_beta)
        first_perp_y = math.sin(first_beta)
        # Length of perpendicular jump to put together head and tail
        well_glued_together = np.sqrt(
            np.square( first_perp_x*(track[0][2] - track[-1][2]) ) +
            np.square( first_perp_y*(track[0][3] - track[-1][3]) ))
        #横ズレを抑える
        if well_glued_together > TRACK_DETAIL_STEP/4:
            #print('false')
            #print('.', end='')
            return False
        #print()
        
        if self.verbose == 1:
            print("Generated {}-tiles track".format(len(track)))
        
        # Create tiles
        road = []
        road_color = []
        for i in range(len(track)):
            alpha1, beta1, x1, y1 = track[i]
            alpha2, beta2, x2, y2 = track[i-1]
            road1_l = (x1 - TRACK_WIDTH*math.cos(beta1), y1 - TRACK_WIDTH*math.sin(beta1))
            road1_r = (x1 + TRACK_WIDTH*math.cos(beta1), y1 + TRACK_WIDTH*math.sin(beta1))
            road2_l = (x2 - TRACK_WIDTH*math.cos(beta2), y2 - TRACK_WIDTH*math.sin(beta2))
            road2_r = (x2 + TRACK_WIDTH*math.cos(beta2), y2 + TRACK_WIDTH*math.sin(beta2))
            road.append([road1_l, road1_r, road2_r, road2_l])
            
            color = ROAD_COLOR[i%2]
            if i == 0:
                road_color.append([0.5, 0.5, 1])
            elif i == len(track) - 1:
                road_color.append([1, 0.5, 0.5])
            else:
                road_color.append(color)
        self.road = np.array(road)
        self.road_color = np.array(road_color)
        return True



    def render(self, mode='plt', dpi=100):
        if mode != 'none':
            #グラフ用意
            fig = plt.figure(figsize=(FIGSIZE, FIGSIZE))
            ax = fig.add_subplot(111)
            ax.set_aspect('equal')
            #plt.rcParams['axes.facecolor'] = BACK_COLOR
            ax.set_facecolor(BACK_COLOR)
            
            
            #道路の描画
            for i in range(len(self.road[:])):
                ax.fill(self.road[i,:,0], self.road[i,:,1], color=self.road_color[i])
                if (i+1) % 10 == 0:
                    center = np.mean(self.road[i], axis=0)
                    textsize = self.TRACK_RAD**0.01 * 8
                    shift = [-self.TRACK_RAD**0.5 * 0.15, -self.TRACK_RAD**0.5 * 0.1]
                    ax.text(center[0]+shift[0], center[1]+shift[1], str(i+1), size=textsize, color='dimgray')
            
            #情報
            plt.title('track_len:{},  track_seed:{} > actual_length:{}m'.format(self.track_len, self.track_seed, int(self.road_len)) )
            ax.plot(0, 0, linestyle='None', label='time   :{}s'.format('{:.1f}'.format(self.t)))
            ax.plot(0, 0, linestyle='None', label='frame  :{}'.format(self.frame + 1))
            ax.plot(0, 0, linestyle='None', label='reward :{}'.format('{:.1f}'.format(self.reward)))
            ax.plot(0, 0, linestyle='None', label='rewards:{}/100'.format('{:.1f}'.format(self.reward_sum)))
            ax.plot(0, 0, linestyle='None', label='visited:{}/{}'.format(self.visited_count, len(self.road)))
            ax.plot(0, 0, linestyle='None', label='speed  :{}m/s'.format('{:.1f}'.format(self.speed)))
            
            ax.legend(handlelength=-0.5, prop={'family':'monospace', 'size':14}, frameon=False)
            
            #車体の描画
            plot_car(self.pos[0], self.pos[1], self.rad, self.carimg, zoom=0.5/self.TRACK_RAD**0.4)#(self.TRACK_RAD**0.005 - 1.015) * 10) 
            #煙の描画
            #plt.plot([self.track[0][1]*100 + self.pos[0], self.pos[0]], [self.track[0][0]*100 + self.pos[1], self.pos[1]], '-k', linewidth=2)
            
            #オーバー領域の更新
            self.road_min[0], self.road_max[0] = ax.get_xlim()
            self.road_min[1], self.road_max[1] = ax.get_ylim()
            
            if mode == 'plt':
                plt.show()
                #print()
            elif mode == 'save':
                print('saving frame {}'.format(self.frame + 1))
                if not os.path.exists('./save'):
                    os.mkdir('./save') #保存フォルダを作成
                plt.savefig('save/{}.png'.format(str(self.frame + 1).zfill(8)), bbox_inches='tight', pad_inches=0, dpi=dpi)
            else:
                pass
            
            plt.close()

        
        
    def step(self, action):
        
        action[0] = np.clip(action[0], -1, 1)
        action[1] = np.clip(action[1], -1, 1)
        
        dt = 1.0/FPS
        
        #向きの速度を更新
        power = 0.4
        self.rad_v += power*action[0]*(min(np.linalg.norm(self.vel), 3.0)/3.0)
        self.rad_v = np.clip(self.rad_v, -1.0*math.pi, 1.0*math.pi)
        self.rad_v *= 0.90
        #向きを更新
        self.rad += dt*self.rad_v
        if self.rad > 2*math.pi:
            self.rad -= 2*math.pi
        if self.rad < 0:
            self.rad += 2*math.pi
        
        #新しい速度ベクトル
        power = 30
        self.v_new = [power*math.sin(-self.rad)*action[1], power*math.cos(self.rad)*action[1]]
        
        #現在の速度ベクトルと新しい速度ベクトルを足す
        rate = 0.02
        self.vel = [(1.0-rate)*self.vel[0] + rate*self.v_new[0], (1.0-rate)*self.vel[1] + rate*self.v_new[1]]
        
        #速度ベクトルを減衰させる要因、車体の向きとベクトルの向きの違い
        x = np.inner(self.vel, self.v_new)
        s = np.linalg.norm(self.vel)
        t = np.linalg.norm(self.v_new)
        theta = np.arccos(x/(s*t))
        if np.isnan(theta):
            theta = 0.0
        
        #減衰
        self.vel[0] *= 0.99**(dt*theta*30)
        self.vel[1] *= 0.99**(dt*theta*30)
        
        #速度で位置を更新
        self.pos[0] += dt*self.vel[0]
        self.pos[1] += dt*self.vel[1]
        
        
        self.speed = (self.vel[0]**2 + self.vel[1]**2)**0.5
        
        #タイル判定
        self.reward = 0.0
        point = Point(self.pos)
        new = False
        #踏んでいないタイルを検索
        for i in range(len(self.road)):
            polygon = Polygon(self.road[i])
            if self.visited[i] == False and polygon.contains(point):
                new = True
                break
        if new == True:
            self.visited[i] = True
            self.visited_count = np.sum(self.visited)
            
            self.reward = 100/len(self.road)
            self.reward_sum = self.visited_count / len(self.road) * 100
            
            self.road_color[i] = (0.9, 0.9, 0.95)
            
        #print(polygon.contains(point), self.visited_count)
        
        #オーバー判定
        over = False
        if not(self.road_min[0] < self.pos[0] < self.road_max[0] and self.road_min[1] < self.pos[1] < self.road_max[1]):
            over = True

        #クリア判定
        done = False
        if self.visited_count == len(self.road):
            done = True
        
        
        self.t += dt
        self.frame += 1
        
        #返り値の準備
        info = {}
        info['position'] = self.pos
        info['velocity'] = self.vel
        info['radian'] = self.rad
        info['radian_v'] = self.rad
        info['road'] = self.road
        info['visited'] = self.visited
        info['visited_count'] = self.visited_count
        info['time'] = self.t
        info['frame'] = self.frame
        info['rewards'] = self.reward_sum
        info['actual_length'] = self.road_len
        info['speed'] = self.speed
        info['road_max'] = self.road_max
        info['road_min'] = self.road_min
        self.state = info
        return self.state, self.reward, over, done





if __name__=="__main__":
    
    env = vcracing(track_len=150, track_seed=5, car=None)
    
    #ステージを固定して初期化
    #state = env.reset(seed=2)
    
    #初期画像を表示
    print(0)
    env.render()
    
    
    
    for i in range(10):
        #print(i)
        action = [0, 1]
        _, _, _, _ = env.step(action)
        env.render()
    '''
    for i in range(8):
        action = [0.35, 1]
        _, _, _, _ = env.step(action)
        env.render()
    for i in range(20):
        #print(i)
        action = [0, 1]
        _, _, _, _ = env.step(action)
        env.render()
    for i in range(13):
        action = [0.8, 1]
        _, _, _, _ = env.step(action)
        env.render()
    for i in range(75):
        action = [0, 1]
        _, _, _, _ = env.step(action)
        env.render()
    for i in range(65):
        action = [0.35, 1]
        _, _, _, _ = env.step(action)
        env.render()
    for i in range(105):
        action = [0, 1]
        _, _, _, _ = env.step(action)
        env.render()
    for i in range(18):
        action = [1, 1]
        _, _, _, _ = env.step(action)
        env.render()
    for i in range(50):
        action = [0, 1]
        _, _, _, _ = env.step(action)
        env.render()
    '''
    '''

    
    
    
    for i in range(3):
        action = [0, 1]
        _, _, done, _ = env.step(action)
        env.render()
    '''
