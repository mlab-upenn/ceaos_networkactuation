""" This file contains all code required to parse and process Network Actuation requests """
import zmq
import logging


class NetworkActuation():
    """ Class that maintains and serves Network Actuation functions """

    def __init__(self, setpoint=None, do=None, port=26462):
        self.setpoint = setpoint
        self.setpoint_conditions = list()
        self.do = do
        self.do_conditions = list()
        self.port = port

    def register_setpoint(self, setpoint_func, dtype=None, rules=None):
        """
        This function registers a setpoint function. Rules are a set of functions, lambda or otherwise, that specify conditions that the arguments must abide by.

        ```python
        NA.register_setpoint(mysetpoint, rules=[lambda x: x<10.0, lambda x: x>0.0])
        ```

        Args:
            setpoint_func (function): Function that accepts a single argument
            dtype (type): Datatype for the argument that goes into setpoint_func
            rules (list): This can be a function or a list of functions that return True or False given the argument that goes into setpoint
        
        """
        import types

        self.setpoint = setpoint_func
        if dtype:
            self.setpoint_conditions += [lambda x: isinstance(x,dtype)]
        if rules:
            self.setpoint_conditions += rules

    def register_do(self, do_func, dtype=None, rules=None):
        """
        This function registers a do function. Rules are a set of functions, lambda or otherwise, that specify conditions that the arguments must abide by.

        ```python
        NA.register_do(mydo, rules=[lambda x: x<10.0, lambda x: x>0.0])
        ```

        Args:
            do_func (function): Function that accepts a single argument
            dtype (type): Datatype for the argument that goes into do_func
            rules (list): This can be a function or a list of functions that return True or False given the argument that goes into setpoint
        
        """
        import types

        self.do = do_func
        if dtype:
            self.do_conditions += [lambda x: isinstance(x,dtype)]
        if rules:
            self.do_conditions += rules

    def listen(self, port=None):
        import json
        
        if port:
            self.port = port

        if port is None:
            raise ValueError("Port not specified")
        
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.bind(f"tcp://*:{port}")

        while True:
            try:
                request = socket.recv()
                message = json.loads(request)  # Parse the request

                try:
                    response = self._parse(message) 
                    
                    logging.info("Request handled: {}".format(request))

                except TypeError as e:
                    response = "Request encountered error: {}".format(e)
                    logging.info(
                        "Request {} encountered payload error {}".format(request, e)
                    )
                
                except ValueError as v:
                    response = "Request encountered error: {}".format(v)
                    logging.info(
                        "Request {} encountered payload error {}".format(request, v)
                    )

                socket.send_string(json.dumps({"response": response, "status": 200}))

            except KeyboardInterrupt:
                # We're being compelled to shutdown. Let's terminate gracefully
                socket.close()
                context.term()

    def _parse(self, message):
        """ Internal method to parse messages """
        from copy import deepcopy

        if "action" not in message:
            raise ValueError("No action declared")
        if "payload" not in message:
            raise ValueError("No target object specified")            
        
        func = None
        rules = None
        if message["action"] == 'setpoint':
            assert(self.setpoint is not None)
            func = self.setpoint
            rules = deepcopy(self.setpoint_conditions)
        elif message["action"] == 'do':
            assert(self.do is not None)
            func = self.do
            rules = deepcopy(self.do_conditions)
        else:
            raise ValueError("Not a valid action")
        
        for i in range(len(rules)):
            rules[i] = rules[i](message['payload'])
        
        if not all(rules):
            raise ValueError("Payload does not comply with ruleset")

        result = func(message['payload'])
        return result
