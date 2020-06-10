standalone = True if os.getenv('ROS_DISTRO') is not None else False
if not standalone:
    from geometry_msgs.msg import TransformStamped
