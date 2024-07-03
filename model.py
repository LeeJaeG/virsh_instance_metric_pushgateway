class InstanceMetrics:
    @staticmethod
    def virtualMachineStats():
        return{
            "state.state": "Virtual_Instance_state",
            "balloon.current": "Virtual_Instance_balloon_current",
            "balloon.maximum": "Virtual_Instance_balloon_maximum",
            "balloon.swap_in": "Virtual_Instance_balloon_swap_in",
            "balloon.swap_out": "Virtual_Instance_balloon_swap_out",
            "balloon.major_fault": "Virtual_Instance_balloon_major_fault",
            "balloon.minor_fault": "Virtual_Instance_balloon_minor_fault",
            "balloon.unused": "Virtual_Instance_balloon_unused",
            "balloon.available": "Virtual_Instance_balloon_available",
            "balloon.rss": "Virtual_Instance_balloon_rss",
            "balloon.usable": "Virtual_Instance_balloon_usable",
        }
    @staticmethod
    def blockModel():
        return{
            "rd_reqs": "block_rd_reqs",
            "rd_bytes": "block_rd_bytes",
            "rd_times": "block_rd_times",
            "wr_reqs": "block_wr_reqs",
            "wr_bytes": "block_wr_bytes",
            "wr_times": "block_wr_times",
            "fl_reqs": "block_fl_reqs",
            "fl_times": "block_fl_times",
            "allocation": "block_allocation",
            "capacity": "block_capacity",
            "physical": "block_physical"
        }
