import pandas as pd
from django.core.management.base import BaseCommand
from django.db import transaction
from portal.models import Department, Organization, Team

class Command(BaseCommand):
    help = "Import everything: Mapping Dependency Type to Team Type"

    def handle(self, *args, **kwargs):
        file_path = "sky_team_registry.xlsx"

        try:
            # 1. Load Excel and clean headers
            df = pd.read_excel(file_path)
            df.columns = [str(c).strip() for c in df.columns]
            
            self.stdout.write(f"Excel Columns detected: {list(df.columns)}")
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"File Error: {e}"))
            return

        # 2. Get/Create the Organization
        org, _ = Organization.objects.get_or_create(name="Axiom Sky Engineering")

        d_count, t_count, u_count = 0, 0, 0

        # 3. Process data
        with transaction.atomic():
            for index, row in df.iterrows():
                # Extract values from Excel
                dept_val = str(row.get('Department', '')).strip()
                team_val = str(row.get('Team', '')).strip()
                # Get "Dependency Type" from Excel
                excel_dep_type = str(row.get('Dependency Type', '')).strip()

                # Validation
                if not dept_val or dept_val.lower() == 'nan':
                    continue

                # --- STEP A: Department ---
                dept, d_created = Department.objects.get_or_create(
                    name=dept_val,
                    organization=org
                )
                if d_created: d_count += 1

                # --- STEP B: Team ---
                if team_val and team_val.lower() != 'nan':
                    # Clean the dependency type value
                    final_type = excel_dep_type if excel_dep_type.lower() != 'nan' else None

                    # update_or_create ensures we don't get duplicates 
                    # and updates the type if it changed in Excel
                    team, t_created = Team.objects.update_or_create(
                        name=team_val,
                        department=dept,
                        defaults={
                            # We map the Excel data to your model field 'team_type'
                            'team_type': final_type 
                        }
                    )
                    
                    if t_created:
                        self.stdout.write(f"Added Team: {team_val} ({final_type})")
                        t_count += 1
                    else:
                        u_count += 1

        # 4. Final Summary
        self.stdout.write(self.style.SUCCESS("\n" + "="*30))
        self.stdout.write(self.style.SUCCESS("IMPORT SUCCESSFUL"))
        self.stdout.write(f"Departments: {d_count}")
        self.stdout.write(f"New Teams:    {t_count}")
        self.stdout.write(f"Updated Teams: {u_count}")
        self.stdout.write(self.style.SUCCESS("="*30))