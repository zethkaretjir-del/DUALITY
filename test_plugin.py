#!/usr/bin/env python3
# Test Plugin System

from core.plugin_manager import PluginManager

def main():
    pm = PluginManager()
    
    while True:
        print("""
╔══════════════════════════════════════╗
║         PLUGIN SYSTEM MENU           ║
╠══════════════════════════════════════╣
║  [1] List available plugins          ║
║  [2] Load plugin                     ║
║  [3] Run plugin                      ║
║  [4] List loaded plugins             ║
║  [5] Unload plugin                   ║
║  [6] Show status                     ║
║  [0] Exit                            ║
╚══════════════════════════════════════╝
        """)
        
        choice = input("Pilih menu: ")
        
        if choice == '1':
            plugins = pm.list_plugins()
            print(f"\n📦 Available plugins: {plugins}")
        
        elif choice == '2':
            name = input("Nama plugin: ")
            module, msg = pm.load_plugin(name)
            print(f"\n{msg}")
        
        elif choice == '3':
            name = input("Nama plugin: ")
            if name in pm.list_loaded():
                result, msg = pm.run_plugin(name)
                print(f"\n📤 Result: {result}")
            else:
                print(f"\n❌ Plugin {name} belum diload")
        
        elif choice == '4':
            loaded = pm.list_loaded()
            print(f"\n🔌 Loaded plugins: {loaded}")
        
        elif choice == '5':
            name = input("Nama plugin: ")
            success, msg = pm.unload_plugin(name)
            print(f"\n{msg}")
        
        elif choice == '6':
            pm.show_status()
        
        elif choice == '0':
            print("👋 Bye!")
            break
        
        input("\nTekan Enter...")

if __name__ == "__main__":
    main()
