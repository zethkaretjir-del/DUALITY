#!/usr/bin/env python3
# AGENT GATEWAY CORE - Central control untuk semua AI agents

import json
import threading
import time
import queue
from datetime import datetime
from core.colors import Colors

class AgentGateway:
    def __init__(self):
        self.name = "Agent Gateway"
        self.agents = {}
        self.task_queue = queue.Queue()
        self.results = {}
        self.running = True
        self.task_history = []
        
        # Register default agents
        self.register_agent("orchestrator", "AI Orchestrator", "master")
        self.register_agent("osint", "OSINT Agent", "worker")
        self.register_agent("vuln", "Vulnerability Agent", "worker")
        self.register_agent("exploit", "Exploit Agent", "worker")
        self.register_agent("payload", "Payload Agent", "worker")
        self.register_agent("report", "Report Agent", "worker")
    
    def register_agent(self, agent_id, agent_name, agent_type="worker"):
        """Register agent ke gateway"""
        self.agents[agent_id] = {
            'id': agent_id,
            'name': agent_name,
            'type': agent_type,
            'status': 'idle',
            'last_active': str(datetime.now()),
            'tasks_completed': 0
        }
        print(f"{Colors.GREEN}[+] Agent registered: {agent_name} ({agent_id}){Colors.END}")
    
    def unregister_agent(self, agent_id):
        """Unregister agent"""
        if agent_id in self.agents:
            del self.agents[agent_id]
            print(f"{Colors.YELLOW}[-] Agent unregistered: {agent_id}{Colors.END}")
    
    def get_agent_status(self, agent_id=None):
        """Get status of agent(s)"""
        if agent_id:
            return self.agents.get(agent_id, None)
        return self.agents
    
    def list_agents(self):
        """List all registered agents"""
        print(f"\n{Colors.CYAN}{'='*55}{Colors.END}")
        print(f"{Colors.BOLD}🤖 REGISTERED AGENTS{Colors.END}")
        print(f"{Colors.CYAN}{'='*55}{Colors.END}")
        
        for agent_id, info in self.agents.items():
            status_color = Colors.GREEN if info['status'] == 'idle' else Colors.YELLOW
            print(f"  {Colors.CYAN}[{agent_id}]{Colors.END} {info['name']}")
            print(f"    Type: {info['type']} | Status: {status_color}{info['status']}{Colors.END}")
            print(f"    Tasks: {info['tasks_completed']} | Last: {info['last_active'][:16]}")
    
    def submit_task(self, agent_id, task_data):
        """Submit task ke agent tertentu"""
        task = {
            'id': f"task_{int(time.time())}_{hash(str(task_data))}",
            'agent_id': agent_id,
            'data': task_data,
            'status': 'queued',
            'submitted_at': str(datetime.now()),
            'completed_at': None,
            'result': None
        }
        self.task_queue.put(task)
        self.task_history.append(task)
        
        print(f"{Colors.GREEN}[+] Task submitted to {agent_id}{Colors.END}")
        return task['id']
    
    def process_tasks(self):
        """Process tasks from queue (background thread)"""
        while self.running:
            try:
                task = self.task_queue.get(timeout=1)
                
                # Update agent status
                if task['agent_id'] in self.agents:
                    self.agents[task['agent_id']]['status'] = 'busy'
                    self.agents[task['agent_id']]['last_active'] = str(datetime.now())
                
                task['status'] = 'processing'
                print(f"{Colors.YELLOW}[*] Processing task: {task['id']} on {task['agent_id']}{Colors.END}")
                
                # Simulate task processing (call actual agent here)
                time.sleep(2)
                
                task['status'] = 'completed'
                task['completed_at'] = str(datetime.now())
                task['result'] = {'success': True, 'message': f'Task completed by {task["agent_id"]}'}
                
                # Update agent stats
                if task['agent_id'] in self.agents:
                    self.agents[task['agent_id']]['tasks_completed'] += 1
                    self.agents[task['agent_id']]['status'] = 'idle'
                
                print(f"{Colors.GREEN}[+] Task completed: {task['id']}{Colors.END}")
                
            except queue.Empty:
                pass
            except Exception as e:
                print(f"{Colors.RED}[!] Task error: {e}{Colors.END}")
    
    def start_gateway(self):
        """Start the gateway (background thread)"""
        self.processor_thread = threading.Thread(target=self.process_tasks, daemon=True)
        self.processor_thread.start()
        print(f"{Colors.GREEN}[+] Agent Gateway started{Colors.END}")
    
    def stop_gateway(self):
        """Stop the gateway"""
        self.running = False
        print(f"{Colors.YELLOW}[-] Agent Gateway stopped{Colors.END}")
    
    def get_statistics(self):
        """Get gateway statistics"""
        stats = {
            'total_agents': len(self.agents),
            'total_tasks': len(self.task_history),
            'completed_tasks': len([t for t in self.task_history if t['status'] == 'completed']),
            'pending_tasks': self.task_queue.qsize(),
            'agents': self.agents
        }
        return stats
    
    def show_dashboard(self):
        """Show gateway dashboard"""
        stats = self.get_statistics()
        
        print(f"\n{Colors.CYAN}{'='*55}{Colors.END}")
        print(f"{Colors.BOLD}📊 AGENT GATEWAY DASHBOARD{Colors.END}")
        print(f"{Colors.CYAN}{'='*55}{Colors.END}")
        print(f"{Colors.WHITE}  Total Agents: {stats['total_agents']}")
        print(f"  Total Tasks: {stats['total_tasks']}")
        print(f"  Completed: {stats['completed_tasks']}")
        print(f"  Pending: {stats['pending_tasks']}{Colors.END}")
        
        # Agent status bar
        print(f"\n{Colors.GREEN}Agent Status:{Colors.END}")
        for agent_id, info in self.agents.items():
            bar = '█' * int(info['tasks_completed'] / 10) if info['tasks_completed'] > 0 else '░'
            print(f"  {agent_id:12} [{bar:10}] {info['tasks_completed']} tasks")
    
    def interactive_mode(self):
        """Interactive gateway control"""
        self.start_gateway()
        
        while True:
            print(f"\n{Colors.CYAN}{'═'*55}{Colors.END}")
            print(f"{Colors.BOLD}🚪 AGENT GATEWAY MENU{Colors.END}")
            print(f"{Colors.CYAN}{'═'*55}{Colors.END}")
            print(f"{Colors.GREEN}[1]{Colors.END} List Agents")
            print(f"{Colors.GREEN}[2]{Colors.END} Submit Task")
            print(f"{Colors.GREEN}[3]{Colors.END} View Dashboard")
            print(f"{Colors.GREEN}[4]{Colors.END} View Task History")
            print(f"{Colors.GREEN}[5]{Colors.END} Register New Agent")
            print(f"{Colors.GREEN}[0]{Colors.END} Exit Gateway")
            
            choice = input(f"\n{Colors.RED}└─{Colors.WHITE}$ {Colors.END}")
            
            if choice == '1':
                self.list_agents()
            
            elif choice == '2':
                print(f"\n{Colors.CYAN}Available agents:{Colors.END}")
                for agent_id in self.agents:
                    print(f"  {Colors.GREEN}• {agent_id}{Colors.END}")
                
                agent_id = input(f"{Colors.GREEN}Agent ID > {Colors.END}")
                task_data = input(f"{Colors.GREEN}Task Data > {Colors.END}")
                
                if agent_id in self.agents:
                    task_id = self.submit_task(agent_id, {'command': task_data})
                    print(f"{Colors.CYAN}Task ID: {task_id}{Colors.END}")
                else:
                    print(f"{Colors.RED}[!] Agent not found!{Colors.END}")
            
            elif choice == '3':
                self.show_dashboard()
            
            elif choice == '4':
                print(f"\n{Colors.CYAN}{'='*55}{Colors.END}")
                print(f"{Colors.BOLD}📜 TASK HISTORY{Colors.END}")
                print(f"{Colors.CYAN}{'='*55}{Colors.END}")
                for task in self.task_history[-10:]:
                    status_color = Colors.GREEN if task['status'] == 'completed' else Colors.YELLOW
                    print(f"  {task['id']} → {task['agent_id']} [{status_color}{task['status']}{Colors.END}]")
            
            elif choice == '5':
                agent_id = input(f"{Colors.GREEN}Agent ID > {Colors.END}")
                agent_name = input(f"{Colors.GREEN}Agent Name > {Colors.END}")
                agent_type = input(f"{Colors.GREEN}Agent Type (master/worker) > {Colors.END}") or "worker"
                self.register_agent(agent_id, agent_name, agent_type)
            
            elif choice == '0':
                self.stop_gateway()
                break
    
    def run(self):
        """Main execution"""
        print(f"\n{Colors.CYAN}[*] {self.name}{Colors.END}")
        self.interactive_mode()

if __name__ == "__main__":
    gateway = AgentGateway()
    gateway.run()
