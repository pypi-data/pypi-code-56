from prometheus_client import CollectorRegistry, Gauge, push_to_gateway



def IO_metrics(push_addr,input,output,input_befor,output_befor,time_differ_list):

    with open("/etc/hostname","r") as f:
        pod_name=f.read()
    registry = CollectorRegistry()
    if len(time_differ_list)==0:
        process_time=0
    else:
        process_time=sum(time_differ_list)/len(time_differ_list)
    input_rate= (input-input_befor)/60
    output_rate=(output-output_befor)/60
    h = Gauge('algorithmIO', '算子IO指标采集', ["io_type"],
              registry=registry)
    h.labels("input").set(input)
    h.labels("output").set(output)
    h.labels("input_rate").set(input_rate)
    h.labels("output_rate").set(output_rate)
    h.labels("process_time").set(process_time)

    push_to_gateway(push_addr, job=pod_name.strip(), registry=h)
    print("push metrics:{input:%s,output:%s,input_rate:%s,output_rate:%s,process_time:%s}"%(input,output,input_rate,output_rate,process_time))
