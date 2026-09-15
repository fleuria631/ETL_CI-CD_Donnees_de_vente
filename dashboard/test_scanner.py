from streamlit.components.v2.component_manager import BidiComponentManager

manager = BidiComponentManager()
manager.discover_and_register_components()
print(manager._manifest_handler._asset_roots)
