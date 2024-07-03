from prometheus_client import CollectorRegistry, Gauge, push_to_gateway
from pydantic import BaseModel
# import openstack
import logging
import uvicorn
from fastapi import FastAPI, Body
from model import InstanceMetrics

app = FastAPI()

# conn = openstack.connect(cloud='openstack')

instance_metric=InstanceMetrics
registry = CollectorRegistry()

state = Gauge('Virtual_Instance_state', 'Virtual_Instance_state', ['instance_id'], registry=registry)
balloon_current = Gauge('Virtual_Instance_balloon_current', 'Virtual_Instance_balloon_current', ['instance_id'], registry=registry)
balloon_maximum = Gauge('Virtual_Instance_balloon_maximum', 'Virtual_Instance_balloon_maximum', ['instance_id'], registry=registry)
balloon_swap_in = Gauge('Virtual_Instance_balloon_swap_in', 'Virtual_Instance_balloon_swap_in', ['instance_id'], registry=registry)
balloon_swap_out = Gauge('Virtual_Instance_balloon_swap_out', 'Virtual_Instance_balloon_swap_out', ['instance_id'], registry=registry)
balloon_major_fault = Gauge('Virtual_Instance_balloon_major_fault', 'Virtual_Instance_balloon_major_fault', ['instance_id'], registry=registry)
balloon_minor_fault = Gauge('Virtual_Instance_balloon_minor_fault', 'Virtual_Instance_balloon_minor_fault', ['instance_id'], registry=registry)
balloon_unused = Gauge('Virtual_Instance_balloon_unused', 'Virtual_Instance_balloon_unused', ['instance_id'], registry=registry)
balloon_available = Gauge('Virtual_Instance_balloon_available', 'Virtual_Instance_balloon_available', ['instance_id'], registry=registry)
balloon_rss = Gauge('Virtual_Instance_balloon_rss', 'Virtual_Instance_balloon_rss', ['instance_id'], registry=registry)
balloon_usable = Gauge('Virtual_Instance_balloon_usable', 'Virtual_Instance_balloon_usable', ['instance_id'], registry=registry)

rd_reqs = Gauge('Virtual_Instance_block_rd_reqs', 'Virtual_Instance_block_rd_reqs', ['instance_id','num'], registry=registry)
rd_bytes = Gauge('Virtual_Instance_block_rd_bytes', 'Virtual_Instance_block_rd_bytes', ['instance_id','num'], registry=registry)
rd_times = Gauge('Virtual_Instance_block_rd_times', 'Virtual_Instance_block_rd_times', ['instance_id','num'], registry=registry)
wr_reqs = Gauge('Virtual_Instance_block_wr_reqs', 'Virtual_Instance_block_wr_reqs', ['instance_id','num'], registry=registry)
wr_bytes = Gauge('Virtual_Instance_block_wr_bytes', 'Virtual_Instance_block_wr_bytes', ['instance_id','num'], registry=registry)
wr_times = Gauge('Virtual_Instance_block_wr_times', 'Virtual_Instance_block_wr_times', ['instance_id','num'], registry=registry)
fl_reqs = Gauge('Virtual_Instance_block_fl_reqs', 'Virtual_Instance_block_fl_reqs', ['instance_id','num'], registry=registry)
fl_times = Gauge('Virtual_Instance_block_fl_times', 'Virtual_Instance_block_fl_times', ['instance_id','num'], registry=registry)
allocation = Gauge('Virtual_Instance_block_allocation', 'Virtual_Instance_block_allocation', ['instance_id','num'], registry=registry)
capacity = Gauge('Virtual_Instance_block_capacity', 'Virtual_Instance_block_capacity', ['instance_id','num'], registry=registry)
physical = Gauge('Virtual_Instance_block_physical', 'Virtual_Instance_block_physical', ['instance_id','num'], registry=registry)


class DomStatsInput(BaseModel):
    domstats_output: object
    domain_uuid: str
    domain_name: str
    disk_num: int

def set_metric_with_default(metric,parsed_data , instance_id, key, default=0):
    try:
        value = parsed_data[key]
    except KeyError:
        value = default
    metric.labels(instance_id=instance_id).set(value)


@app.post('/endpoint')
async def receive_post(contents: list = Body(...)):
    # server_list = list(conn.compute.servers(all_projects=False))
    
    
    for content in contents: 
        lines = dict(content)['domstats_output'].strip().split('\n')

    # Create a dictionary to store the parsed data
        parsed_data = {'Domain': lines[0].split("'")[1]}
        
        

    # Iterate over the remaining lines and add key-value pairs to the dictionary
        for line in lines[1:]:
            key, value = map(str.strip, line.split('='))
            parsed_data[key] = int(value) if value.isdigit() else value


        
    # Print the resulting dictionary

        state.labels(instance_id=content['domain_uuid']).set(parsed_data['state.state'])
        balloon_current.labels(instance_id=content['domain_uuid']).set(parsed_data['balloon.current'])
        balloon_maximum.labels(instance_id=content['domain_uuid']).set(parsed_data['balloon.maximum'])
        try:
            balloon_swap_in.labels(instance_id=content['domain_uuid']).set(parsed_data['balloon.swap_in'])
            balloon_swap_out.labels(instance_id=content['domain_uuid']).set(parsed_data['balloon.swap_out'])
            balloon_major_fault.labels(instance_id=content['domain_uuid']).set(parsed_data['balloon.major_fault'])
            balloon_minor_fault.labels(instance_id=content['domain_uuid']).set(parsed_data['balloon.minor_fault'])
            balloon_unused.labels(instance_id=content['domain_uuid']).set(parsed_data['balloon.unused'])
            balloon_available.labels(instance_id=content['domain_uuid']).set(parsed_data['balloon.available'])
            balloon_rss.labels(instance_id=content['domain_uuid']).set(parsed_data['balloon.rss'])
            balloon_usable.labels(instance_id=content['domain_uuid']).set(parsed_data['balloon.usable'])
        except KeyError:
            pass
        for i in range(0,dict(content)['disk_num']+1):
            try:
                rd_reqs.labels(instance_id=content['domain_uuid'],num=i).set(parsed_data['block.'+str(i)+'.rd.reqs'])
                rd_bytes.labels(instance_id=content['domain_uuid'],num=i).set(parsed_data['block.'+str(i)+'.rd.bytes'])
                rd_times.labels(instance_id=content['domain_uuid'],num=i).set(parsed_data['block.'+str(i)+'.rd.times'])
                wr_reqs.labels(instance_id=content['domain_uuid'],num=i).set(parsed_data['block.'+str(i)+'.wr.reqs'])
                wr_bytes.labels(instance_id=content['domain_uuid'],num=i).set(parsed_data['block.'+str(i)+'.wr.bytes'])
                wr_times.labels(instance_id=content['domain_uuid'],num=i).set(parsed_data['block.'+str(i)+'.wr.times'])
                fl_reqs.labels(instance_id=content['domain_uuid'],num=i).set(parsed_data['block.'+str(i)+'.fl.reqs'])
                fl_times.labels(instance_id=content['domain_uuid'],num=i).set(parsed_data['block.'+str(i)+'.fl.times'])
                allocation.labels(instance_id=content['domain_uuid'],num=i).set(parsed_data['block.'+str(i)+'.allocation'])
                capacity.labels(instance_id=content['domain_uuid'],num=i).set(parsed_data['block.'+str(i)+'.capacity'])
                physical.labels(instance_id=content['domain_uuid'],num=i).set(parsed_data['block.'+str(i)+'.physical'])
            except KeyError:
                pass
        push_to_gateway('192.168.15.21:9091', job='virtual_machine_exporter', registry=registry,)

    
    return f"Received POST data: {content}"

    
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, loop='uvloop', reload=True)
