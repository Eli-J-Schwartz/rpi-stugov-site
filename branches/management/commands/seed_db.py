import random
import string

from branches.models import (
    Role, 
    MemberProfile, 
    MemberRoleAssignment, 
    RoleConfig, 
    MembershipDisplay, 
    BranchPage,
    MemberListingPage,
    BranchRoleConfig,
    CommitteeIndexPage,
    CommitteePage,
    CommitteeRoleConfig,
    CommitteeMemberPlacement,
    ClassCouncilIndexPage,
    ClassCouncilPage,
    ClassCouncilRoleConfig,
    FlexiblePage,
    class_choices
)

from wagtail.models import Page

db_classes = [
    Role, 
    MemberProfile, 
    MemberRoleAssignment,
    BranchPage,
    ClassCouncilPage,
    ClassCouncilIndexPage,
    ClassCouncilRoleConfig,
    MemberListingPage,
    BranchRoleConfig
]

from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = "Seed database with randomly generated data."

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear the existing data from the database.",
        )
        
    def handle(self, *args, **options):
        if options["clear"]:
            for db_class in db_classes:
                print(f"deleted all {db_class}")
                db_class.objects.all().delete()

        root_page = Page.objects.get(title="Home").specific

        uc_branch_page = BranchPage(
            branch_type="uc",
            tagline="The undergraduate council branch of student government.",
            image=None,
            image_credit="",
            image_credit_url="",
            body=[],
            contact_email="uc@rpi.edu",
            meeting_schedule="",
            title="Undergraduate Council",
            slug="uc",
            show_in_menus=True
        )

        root_page.add_child(instance=uc_branch_page)

        class_council_list_page = ClassCouncilIndexPage(
            title="Class Council Index",
            slug="class_council_index",
            intro="Index of all class councils.",
            show_in_menus=True
        )

        uc_branch_page.add_child(instance=class_council_list_page)

        uc_member_page = MemberListingPage(
            title="Undergraduate Council Member List",
            slug="uc_member_list",
            intro="The members of the Undergraduate Council.",
            show_in_menus=True
        )

        uc_branch_page.add_child(instance=uc_member_page)

        name = f"Undergraduate President"
        role, created = Role.objects.update_or_create(
            name=name,
            defaults={
                "name": name,
                "positions": 1,
                "constituency": 'none',
            }
        )
        if created: print(f"Created {name}")
        new_person = self.make_person(class_choices()[0][0])
        MemberRoleAssignment.objects.create(
            member=new_person,
            role=role
        )
        BranchRoleConfig.objects.create(
            role=role,
            role_display="President",
            hierarchy_tier=0,
            page=uc_member_page
        )

        name = f"Undergraduate Vice President"
        role, created = Role.objects.update_or_create(
            name=name,
            defaults={
                "name": name,
                "positions": 1,
                "constituency": 'none',
            }
        )
        if created: print(f"Created {name}")
        new_person = self.make_person(class_choices()[0][0])
        MemberRoleAssignment.objects.create(
            member=new_person,
            role=role
        )
        BranchRoleConfig.objects.create(
            role=role,
            role_display="Vice President",
            hierarchy_tier=1,
            page=uc_member_page
        )

        for officer in ["Secretary", "Treasurer", "Publicity Director"]:
            name = f"[UC] {officer}"
            role, created = Role.objects.update_or_create(
                name=name,
                defaults={
                    "name": name,
                    "positions": 1,
                    "constituency": 'none',
                }
            )
            if created: print(f"Created {name}")
            new_person = self.make_person(class_choices()[0][0])
            MemberRoleAssignment.objects.create(
                member=new_person,
                role=role
            )
            BranchRoleConfig.objects.create(
                role=role,
                role_display=f"{officer}",
                hierarchy_tier=1,
                page=uc_member_page
            )

        for class_num, _ in class_choices():
            if class_num == "graduate": continue
            
            class_council_page = ClassCouncilPage(
                title=f"Class of {class_num} Council",
                slug=f"{class_num}_class_council",
                class_year=class_num,
                description=f"The class council for the class of {class_num}."
            )
    
            class_council_list_page.add_child(instance=class_council_page)
            
            name = f"[{class_num}] Class of {class_num} Representative"
            role, created = Role.objects.update_or_create(
                name=name,
                defaults={
                    "name": name,
                    "positions": 8,
                    "constituency": class_num,
                }
            )
            if created: print(f"Created {name}")

            for i in range(8):
                new_person = self.make_person(class_num)
                MemberRoleAssignment.objects.create(
                    member=new_person,
                    role=role
                )

            ClassCouncilRoleConfig.objects.create(
                role=role,
                role_display="Class Representative",
                hierarchy_tier=3,
                page=class_council_page
            )
            
            name = f"Class of {class_num} Senator"
            role, created = Role.objects.update_or_create(
                name=name,
                defaults={
                    "name": name,
                    "positions": 4,
                    "constituency": class_num,
                }
            )
            if created: print(f"Created {name}")

            for i in range(4):
                new_person = self.make_person(class_num)
                MemberRoleAssignment.objects.create(
                    member=new_person,
                    role=role
                )
                
            ClassCouncilRoleConfig.objects.create(
                role=role,
                role_display="Class Senator",
                hierarchy_tier=3,
                page=class_council_page
            )
            
            name = f"Class of {class_num} President"
            role, created = Role.objects.update_or_create(
                name=name,
                defaults={
                    "name": name,
                    "positions": 1,
                    "constituency": 'none',
                }
            )
            if created: print(f"Created {name}")

            for i in range(1):
                new_person = self.make_person(class_num)
                MemberRoleAssignment.objects.create(
                    member=new_person,
                    role=role
                )

            ClassCouncilRoleConfig.objects.create(
                role=role,
                role_display="Class Vice President",
                hierarchy_tier=1,
                page=class_council_page
            )
            BranchRoleConfig.objects.create(
                role=role,
                role_display=f"Class of {class_num} Vice President",
                hierarchy_tier=3,
                page=uc_member_page
            )
            
            name = f"Class of {class_num} Vice President"
            role, created = Role.objects.update_or_create(
                name=name,
                defaults={
                    "name": name,
                    "positions": 1,
                    "constituency": 'none',
                }
            )
            if created: print(f"Created {name}")

            for i in range(1):
                new_person = self.make_person(class_num)
                MemberRoleAssignment.objects.create(
                    member=new_person,
                    role=role
                )

            ClassCouncilRoleConfig.objects.create(
                role=role,
                role_display="Class President",
                hierarchy_tier=0,
                page=class_council_page
            )
            BranchRoleConfig.objects.create(
                role=role,
                role_display=f"Class of {class_num} President",
                hierarchy_tier=3,
                page=uc_member_page
            )

            for officer_role in ["Secretary", "Treasurer", "Publicity Director"]:
                name = f"[{class_num}] {officer_role}"
                role, created = Role.objects.update_or_create(
                    name=name,
                    defaults={
                        "name": name,
                        "positions": 1,
                        "constituency": 'none',
                    }
                )
                new_person = self.make_person(class_num)
                MemberRoleAssignment.objects.create(
                    member=new_person,
                    role=role
                )
                ClassCouncilRoleConfig.objects.create(
                    role=role,
                    role_display=officer_role,
                    hierarchy_tier=1,
                    page=class_council_page
                )
                if created: print(f"Created {name}")

    emails = []
    def make_email(self):
        while True:
            email = ''.join([random.choice(string.ascii_lowercase) for _ in range(6)]) + str(random.randint(2,20)) + "@rpi.edu"
            if email not in self.emails: 
                self.emails.append(email)
                return email
    
    def make_person(self, year):
        email = self.make_email()
        person, _ = MemberProfile.objects.update_or_create(
            email=email,
            defaults={
                "first_name": ''.join([random.choice(string.ascii_lowercase) for _ in range(7)]).capitalize(),
                "last_name": ''.join([random.choice(string.ascii_lowercase) for _ in range(10)]).capitalize(),
                "email": email,
                "class_year": year,
                "major": ''.join([random.choice(string.ascii_uppercase) for _ in range(4)]),
                "bio": ''.join([random.choice(string.ascii_lowercase+"                            .") for _ in range(100)])
            }
        )
        return person
        
        
        # try:
        #     with open(csv_path, newline="", encoding="utf-8-sig") as f:
        #         rows = list(csv.DictReader(f))
        # except FileNotFoundError:
        #     raise CommandError(f"File not found: {csv_path}")

        # if not rows:
        #     raise CommandError("CSV file is empty (no data rows).")

        # missing = REQUIRED_COLUMNS - set(rows[0].keys())
        # if missing:
        #     raise CommandError(
        #         f"CSV is missing required columns: {', '.join(sorted(missing))}"
        #     )

        # if clear and not dry_run:
        #     count = MemberProfile.objects.all().delete()[0]
        #     self.stdout.write(
        #         self.style.WARNING(f"Cleared {count} existing placements.")
        #     )

        # # -- Process rows --
        # stats = {
        #     "created": 0,
        #     "updated": 0,
        #     "errors": 0,
        # }

        # for i, row in enumerate(rows, start=2):  # start=2 because row 1 is header
        #     row = {k: (v or "").strip() for k, v in row.items()}
        #     first_name = row.get("first_name", "")
        #     last_name = row.get("last_name", "")
        #     rcs_id = row.get("rcs_id", "")

        #     if not first_name or not last_name:
        #         self.stderr.write(
        #             self.style.ERROR(f"Row {i}: missing first or last name, skipping.")
        #         )
        #         stats["errors"] += 1
        #         continue
        #     if not rcs_id:
        #         self.stderr.write(
        #             self.style.ERROR(f"Row {i}: missing rcs_id, skipping.")
        #         )
        #         stats["errors"] += 1
        #         continue

        #     if dry_run:
        #         if use_names:
        #             exists = MemberProfile.objects.filter(
        #                 first_name__iexact=first_name,
        #                 last_name__iexact=last_name,
        #             ).exists()
        #             action = "update" if exists else "create"
        #             self.stdout.write(
        #                 f"Row {i}: would {action} profile '{first_name} {last_name}' "
        #             )
        #         else:
        #             exists = MemberProfile.objects.filter(
        #                 email__iexact=f"{rcs_id}@rpi.edu",
        #             ).exists()
        #             action = "update" if exists else "create"
        #             self.stdout.write(
        #                 f"Row {i}: would {action} profile '{rcs_id}' "
        #             )
        #         stats["created" if action == "create" else "updated"] += 1
        #         continue

        #     profile_defaults = {
        #         "first_name": first_name,
        #         "last_name": last_name,
        #         "email": f"{rcs_id}@rpi.edu",
        #     }
        #     if row.get("class_year"):
        #         profile_defaults["class_year"] = row["class_year"]
        #     if row.get("major"):
        #         profile_defaults["major"] = row["major"]
        #     if row.get("bio"):
        #         profile_defaults["bio"] = row["bio"]

        #     if use_names:
        #         _, created = MemberProfile.objects.update_or_create(
        #             first_name__iexact=first_name,
        #             last_name__iexact=last_name,
        #             defaults=profile_defaults,
        #         )
        #     else:
        #         _, created = MemberProfile.objects.update_or_create(
        #             email__iexact=f"{rcs_id}@rpi.edu",
        #             defaults=profile_defaults,
        #         )
        #     stats["created" if created else "updated"] += 1

        # # -- Summary --
        # prefix = "[DRY RUN] " if dry_run else ""
        # self.stdout.write("")
        # self.stdout.write(self.style.SUCCESS(f"{prefix}Member profile import complete:"))
        # self.stdout.write(f"  Profiles created:   {stats['created']}")
        # self.stdout.write(f"  Profiles updated:   {stats['updated']}")
        # if stats["errors"]:
        #     self.stdout.write(
        #         self.style.ERROR(f"  Errors:             {stats['errors']}")
        #     )
