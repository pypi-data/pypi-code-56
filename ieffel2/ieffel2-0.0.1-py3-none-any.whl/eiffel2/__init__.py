def builder(list,bmode =" "):
    """
    Creates a Neural network diagram
    """

    import turtle
    turtle.clear()
   # Default Colors
    b_color = 'white'
    pen_color = '#1B2631'

    screen = turtle.Screen()
    screen.title("EIFFEL: NEURAL NETWORK BUILDER")
    screen.setup(width=400,height=400)
    win_width, win_height= 2000, 2000
    turtle.setup()
    turtle.screensize(win_width, win_height)


    if bmode == "night":
        pen_color ="white"
        b_color = ('#1B2631')

    screen.bgcolor(b_color)

    pen = turtle.Turtle()
    pen.hideturtle()
    pen.color(pen_color)
    turtle.color(b_color)
    pen.speed(-1)
    pen.width(0.5)

    def byebye():
        screen.bye()

    ### NODES ####

    sub =0
    y=250
    x = -250
    y_history=[]
    x_history=[]
    architecture = list #[10,5,5,5,5,5,10,2,2,2] #[20,10,10,10,5,2,2,1]
    for j in range(len(architecture)):
        if j != 0:
            try:
                sub = 10* (architecture[j-1] - architecture[j])

            except:
                pass

        y = y - sub
        y_cache = y
        x +=70
        for i in range(architecture[j]):
            y_history.append(y)
            x_history.append(x)
            y -= 20
            pen.speed(0)
            pen.penup()
            pen.setpos((x  ,y))
            pen.pendown()
            pen.circle(10)
        y = y_cache

    ### EDGES ####

    p1=0
    p2=0
    p3=0
    for j in range(0,len(architecture)-1):
        p2+=architecture[j]
        p3=architecture[j+1]

        for i in range(p1,p2):
            for a in range(p3):
                pen.penup()
                pen.setpos((x_history[i]+10,y_history[i]-10))
                pen.down()
                pen.setpos((x_history[p2+a]-5,y_history[p2+a]-10))

        p1+=architecture[j]



    turtle.listen() # enable turtle to wait for prevents
    turtle.onkey(byebye,"e")
    turtle.exitonclick()
