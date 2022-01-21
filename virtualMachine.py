from client import AzureClient



class VirtualMachine:
    def __init__(self):
        self._compute_client = AzureClient().compute_client()


    def stop(self, vm, auth_data):
        return self.vm_action(vm, 'stop')

    def start(self, vm, auth_data):
        return self.vm_action(vm, 'start')

    def reboot(self, vm, auth_data):
        return self.vm_action(vm, 'reboot')

    def vm_action(self, vm, action):
        try:
            group_name = vm.id.split('/')[0]
            vm_name = vm.id.split('/')[1]

            if action == 'stop':
                self._compute_client.virtual_machines.power_off(group_name, vm_name)
            elif action == 'start':
                self._compute_client.virtual_machines.start(group_name, vm_name)
            elif action == 'reboot':
                self._compute_client.virtual_machines.restart(group_name, vm_name)
        except Exception as ex:
            self.log_exception("Error restarting the VM")
            return False, "Error restarting the VM: " + str(ex)

        return True, ""


    def alterVM(self, vm, radl, auth_data):
        try:
            group_name = vm.id.split('/')[0]
            vm_name = vm.id.split('/')[1]


            # Deallocating the VM (resize prepare)
            async_vm_deallocate = self._compute_client.virtual_machines.deallocate(group_name, vm_name)
            async_vm_deallocate.wait()

            instance_type = self.get_instance_type(radl.systems[0], credentials, subscription_id)
            vm_parameters = " { 'hardware_profile': { 'vm_size': %s } } " % instance_type.name

            async_vm_update = self._compute_client.virtual_machines.create_or_update(group_name,
                                                                               vm_name,
                                                                               vm_parameters)
            async_vm_update.wait()

            # Start the VM
            async_vm_start = self._compute_client.virtual_machines.start(group_name, vm_name)
            async_vm_start.wait()

            return self.updateVMInfo(vm, auth_data)
        except Exception as ex:
            self.log_exception("Error altering the VM")
            return False, "Error altering the VM: " + str(ex)

        return (True, "")