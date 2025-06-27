# src/analysis/folder_analyzer.py
from datetime import datetime
import pandas as pd

class FolderAnalyzer:
    """
    Analyzes Formstack folder data, extracting key information like
    folder hierarchy, form counts, and other folder metrics.
    """
    def __init__(self, formstack_client):
        """
        Initializes the FolderAnalyzer with a FormstackClient instance.

        Args:
            formstack_client: An instance of FormstackClient to make API calls.
        """
        self.client = formstack_client

    def _parse_formstack_date(self, date_string):
        """
        Parses a Formstack API date string (e.g., "YYYY-MM-DD HH:MM:SS") into a datetime object.
        Uses pandas.to_datetime for robustness.

        Args:
            date_string (str): The date string from Formstack API.

        Returns:
            datetime.datetime or pd.NaT: The parsed datetime object, or pd.NaT if parsing fails.
        """
        if not date_string:
            return pd.NaT
        try:
            return pd.to_datetime(date_string, errors='coerce')
        except Exception as e:
            print(f"Warning: Could not parse date string '{date_string}': {e}")
            return pd.NaT

    def get_folder_summary_data(self):
        """
        Fetches all folders and forms, then creates a comprehensive folder summary
        including hierarchy information and form counts.

        Returns:
            list: A list of dictionaries, where each dictionary contains
                  summary information for a folder (id, name, parent_id,
                  parent_name, subfolders, form_count, etc.)
        """
        try:
            # Fetch raw data from Formstack API using the complete hierarchy method
            folders_data = self.client.get_complete_folder_hierarchy()
            forms_data = self.client.get_all_forms()
            
            if not folders_data:
                print("No folders data received from Formstack API.")
                return []

            print(f"Processing {len(folders_data)} folders...")
            
            # Debug: Log the structure of the first folder to understand the data format
            if folders_data:
                print(f"Sample folder data structure: {list(folders_data[0].keys())}")
                print(f"First folder: {folders_data[0]}")
            
            # Create a mapping for easier parent/child lookups
            folder_map = {folder['id']: folder for folder in folders_data}
            
            # Count forms in each folder
            folder_form_counts = {}
            for form in forms_data:
                folder_id = form.get('folder')
                if folder_id:
                    folder_form_counts[folder_id] = folder_form_counts.get(folder_id, 0) + 1

            # Build folder summary data
            folder_summary = []
            
            for folder in folders_data:
                try:
                    folder_id = folder.get('id')
                    folder_name = folder.get('name', 'Unnamed Folder')
                    parent_id = folder.get('parent', None)
                    
                    # Get parent folder name if it exists
                    parent_name = None
                    if parent_id and parent_id in folder_map:
                        parent_name = folder_map[parent_id].get('name', 'Unknown Parent')
                    
                    # Find subfolders
                    subfolders = []
                    for other_folder in folders_data:
                        if other_folder.get('parent') == folder_id:
                            subfolders.append({
                                'id': other_folder.get('id'),
                                'name': other_folder.get('name', 'Unnamed Subfolder')
                            })
                    
                    # Get form count for this folder
                    form_count = folder_form_counts.get(folder_id, 0)
                    
                    # Parse created date if available - check multiple possible field names
                    created_at = None
                    possible_date_fields = ['created', 'created_at', 'date_created', 'timestamp']
                    for field in possible_date_fields:
                        if field in folder and folder[field]:
                            created_at = self._parse_formstack_date(folder[field])
                            break
                    
                    # If no date found, set to None (will be handled as pd.NaT in pandas)
                    if created_at is None:
                        created_at = pd.NaT
                    
                    # Build the folder summary record
                    folder_record = {
                        'id': folder_id,
                        'name': folder_name,
                        'parent_id': parent_id,
                        'parent_name': parent_name,
                        'is_root_folder': parent_id is None,
                        'subfolder_count': len(subfolders),
                        'subfolders': subfolders,
                        'form_count': form_count,
                        'created_at': created_at,
                        'folder_path': self._build_folder_path(folder_id, folder_map),
                        'depth_level': self._calculate_folder_depth(folder_id, folder_map)
                    }
                    
                    folder_summary.append(folder_record)
                    
                except Exception as e:
                    print(f"Error processing folder {folder.get('id', 'unknown')}: {e}")
                    # Continue processing other folders
                    continue
            
            print(f"Successfully processed {len(folder_summary)} folders.")
            return folder_summary
        
        except Exception as e:
            print(f"Error in get_folder_summary_data: {e}")
            return []

    def _build_folder_path(self, folder_id, folder_map):
        """
        Builds a hierarchical path for a folder (e.g., "Parent > Child > Grandchild").
        
        Args:
            folder_id: The ID of the folder to build path for
            folder_map: Dictionary mapping folder IDs to folder data
            
        Returns:
            str: The hierarchical path of the folder
        """
        path_parts = []
        current_id = folder_id
        max_depth = 10  # Prevent infinite loops
        depth = 0
        
        while current_id and depth < max_depth:
            if current_id in folder_map:
                folder = folder_map[current_id]
                path_parts.insert(0, folder.get('name', 'Unknown'))
                current_id = folder.get('parent')
            else:
                break
            depth += 1
        
        return ' > '.join(path_parts) if path_parts else 'Root'

    def _calculate_folder_depth(self, folder_id, folder_map):
        """
        Calculates the depth level of a folder in the hierarchy (0 = root).
        
        Args:
            folder_id: The ID of the folder to calculate depth for
            folder_map: Dictionary mapping folder IDs to folder data
            
        Returns:
            int: The depth level (0 for root folders)
        """
        depth = 0
        current_id = folder_id
        max_depth = 10  # Prevent infinite loops
        
        while current_id and depth < max_depth:
            if current_id in folder_map:
                folder = folder_map[current_id]
                parent_id = folder.get('parent')
                if parent_id:
                    depth += 1
                    current_id = parent_id
                else:
                    break
            else:
                break
        
        return depth

    def get_folder_stats(self):
        """
        Gets general statistics about folders.
        
        Returns:
            dict: Statistics about folders (total count, root folders, etc.)
        """
        try:
            folders_data = self.client.get_all_folders()
            forms_data = self.client.get_all_forms()
            
            if not folders_data:
                return {
                    'total_folders': 0,
                    'root_folders': 0,
                    'folders_with_forms': 0,
                    'total_forms_in_folders': 0
                }
            
            # Count forms in folders
            folders_with_forms = set()
            total_forms_in_folders = 0
            
            for form in forms_data:
                folder_id = form.get('folder')
                if folder_id:
                    folders_with_forms.add(folder_id)
                    total_forms_in_folders += 1
            
            # Count root folders
            root_folders = sum(1 for folder in folders_data if not folder.get('parent'))
            
            return {
                'total_folders': len(folders_data),
                'root_folders': root_folders,
                'folders_with_forms': len(folders_with_forms),
                'total_forms_in_folders': total_forms_in_folders
            }
        
        except Exception as e:
            print(f"Error getting folder stats: {e}")
            return {
                'total_folders': 0,
                'root_folders': 0,
                'folders_with_forms': 0,
                'total_forms_in_folders': 0
            }
