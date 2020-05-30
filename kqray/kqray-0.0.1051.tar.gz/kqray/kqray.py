import math


class RayCaster():
    def cast_ray(array, object_pass, x, y, angle, start_speed, end_speed):
        '''
        ----------------------------------
        |THANKS FOR USING MY RAYCASTER :)|
        |---------------------------------
        |
        |
        The function accepts
        1) 2D array of numbers / strings
        2) Invisible objects
        3) the x-Coordinate of the object emitting the beam
        4) the y Coordinate of the object emitting the beam
        5) the Angle at which the beam will go (in radians)
        6) the Initial velocity of the beam *
        7) the Final speed of the beam *
        * Under numbers 6 and 7, the values needed to optimize the
        raycasting (the Ray goes at the speed specified under
        number 6, and as soon as it collides with the object, it
        goes back one step, and goes at speed 7 (speed7 < speed6),
        and you can get a better calculation quality for less cost of CPU power)
        |
        |
        |
        The function returns
        1) name of the object (which the beam encountered)
        2) the length of the path traversed by the beam
        3) the difference between the int beam coordinate and the float beam
        |---coordinate (if you are going to make an engine using this raycaster,
        |---this is suitable for determining the wall texture by x)
        4) the side that the beam collided with (true = "vertical",
        |---false= "horizontal")
        '''
        rayx    = x
        rayy    = y
        ray_len = 0
        speed   = start_speed
        obj     = None

        while obj in object_pass or obj is None:
            ray_len += speed
            rayy     = y + ray_len * math.sin(angle)
            rayx     = x + ray_len * math.cos(angle)
            obj      = array[int(rayy)][int(rayx)]
            if obj in object_pass and speed == start_speed:
                ray_len -= speed
                speed    = end_speed
                obj      = None

        xside = True
        if array[int(rayy - math.sin(angle) * speed)][int(rayx)] ==\
           array[int(rayy + math.sin(angle) * speed)][int(rayx)]:
            xside = False

        if xside:
            if y > rayy: 
                cut = 1 - rayx + int(rayx)
            else:
                cut = rayx - int(rayx)
        else:
            if x < rayx: 
                cut = 1 - rayy + int(rayy)
            else:
                cut = rayy - int(rayy)

        return obj, ray_len, cut, xside
