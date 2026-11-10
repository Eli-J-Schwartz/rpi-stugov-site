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

from forms_ext.models import (
    ComplaintFormPage,
    FormField
)

from records.models import (
    RecordIndexPage
)

from rep_finder.models import (
    RepsFormPage
)

from home.models import (
    SiteSettings
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
    BranchRoleConfig,
    CommitteePage,
    CommitteeIndexPage,
    CommitteeMemberPlacement,
    CommitteeRoleConfig,
    RepsFormPage,
    RecordIndexPage,
    ComplaintFormPage
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

        random.seed(12180)

        senators_list = []

        root_page = Page.objects.get(title="Home").specific

        senate_branch_page = BranchPage(
            branch_type="senate",
            tagline="The senate branch of student government.",
            image=None,
            image_credit="",
            image_credit_url="",
            body=[],
            contact_email="gm@rpi.edu",
            meeting_schedule="",
            title="Senate",
            slug="senate",
            show_in_menus=True
        )

        root_page.add_child(instance=senate_branch_page)

        senate_member_page = MemberListingPage(
            title="Senate Member List",
            slug="senate_member_list",
            intro="The members of the Senate.",
            show_in_menus=True
        )
        
        senate_branch_page.add_child(instance=senate_member_page)

        senate_committee_page = CommitteeIndexPage(
            title="Senate Committeee List",
            slug="senate_committee_list",
            intro="The committees of the Senate.",
            show_in_menus=True
        )

        senate_branch_page.add_child(instance=senate_committee_page)

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
                senators_list.append(new_person)
                
            ClassCouncilRoleConfig.objects.create(
                role=role,
                role_display="Class Senator",
                hierarchy_tier=3,
                page=class_council_page
            )
            BranchRoleConfig.objects.create(
                role=role,
                role_display=f"Class of {class_num} Senator",
                hierarchy_tier=3,
                page=senate_member_page
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

        gc_branch_page = BranchPage(
            branch_type="gc",
            tagline="The graduate council branch of student government.",
            image=None,
            image_credit="",
            image_credit_url="",
            body=[],
            contact_email="gc@rpi.edu",
            meeting_schedule="",
            title="Graduate Council",
            slug="gc",
            show_in_menus=True
        )

        root_page.add_child(instance=gc_branch_page)

        gc_member_page = MemberListingPage(
            title="Graduate Council Member List",
            slug="gc_member_list",
            intro="The members of the Graduate Council.",
            show_in_menus=True
        )

        gc_branch_page.add_child(instance=gc_member_page)
                        
        name = f"Graduate Representative"
        role, created = Role.objects.update_or_create(
            name=name,
            defaults={
                "name": name,
                "positions": 8,
                "constituency": 'graduate',
            }
        )
        if created: print(f"Created {name}")

        for i in range(8):
            new_person = self.make_person('graduate')
            MemberRoleAssignment.objects.create(
                member=new_person,
                role=role
            )

        BranchRoleConfig.objects.create(
            role=role,
            role_display="Graduate Representative",
            hierarchy_tier=3,
            page=gc_member_page
        )
        
        name = f"Graduate Senator"
        role, created = Role.objects.update_or_create(
            name=name,
            defaults={
                "name": name,
                "positions": 4,
                "constituency": 'graduate',
            }
        )
        if created: print(f"Created {name}")

        for i in range(4):
            new_person = self.make_person('graduate')
            MemberRoleAssignment.objects.create(
                member=new_person,
                role=role
            )
            senators_list.append(new_person)
            
        BranchRoleConfig.objects.create(
            role=role,
            role_display="Graduate Senator",
            hierarchy_tier=3,
            page=gc_member_page
        )
        BranchRoleConfig.objects.create(
            role=role,
            role_display=f"Graduate Senator",
            hierarchy_tier=3,
            page=senate_member_page
        )
        
        name = f"Graduate Vice President"
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
            new_person = self.make_person('graduate')
            MemberRoleAssignment.objects.create(
                member=new_person,
                role=role
            )

        BranchRoleConfig.objects.create(
            role=role,
            role_display="Graduate Vice President",
            hierarchy_tier=1,
            page=gc_member_page
        )
        
        name = f"Graduate President"
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
            new_person = self.make_person('graduate')
            MemberRoleAssignment.objects.create(
                member=new_person,
                role=role
            )

        BranchRoleConfig.objects.create(
            role=role,
            role_display="Graduate President",
            hierarchy_tier=0,
            page=gc_member_page
        )

        for officer_role in ["Secretary", "Treasurer", "Publicity Director"]:
            name = f"[GC] {officer_role}"
            role, created = Role.objects.update_or_create(
                name=name,
                defaults={
                    "name": name,
                    "positions": 1,
                    "constituency": 'none',
                }
            )
            new_person = self.make_person('graduate')
            MemberRoleAssignment.objects.create(
                member=new_person,
                role=role
            )
            BranchRoleConfig.objects.create(
                role=role,
                role_display=officer_role,
                hierarchy_tier=1,
                page=gc_member_page
            )
            if created: print(f"Created {name}")

        for officer_role in ["Secretary", "Treasurer", "Parlimenatarian"]:
            name = f"[Senate] {officer_role}"
            role, created = Role.objects.update_or_create(
                name=name,
                defaults={
                    "name": name,
                    "positions": 1,
                    "constituency": 'none',
                }
            )
            new_person = self.make_person(class_choices()[0][0])
            MemberRoleAssignment.objects.create(
                member=new_person,
                role=role
            )
            BranchRoleConfig.objects.create(
                role=role,
                role_display=officer_role,
                hierarchy_tier=1,
                page=senate_member_page
            )
            if created: print(f"Created {name}")

        name = f"Grand Marshall"
        role, created = Role.objects.update_or_create(
            name=name,
            defaults={
                "name": name,
                "positions": 1,
                "constituency": 'none',
            }
        )
        new_person = self.make_person(class_choices()[0][0])
        MemberProfile.objects.filter(email=new_person.email).update(
            first_name = "Ben",
            last_name = "Bitdiddle",
            email = "bitdib@rpi.edu"   
        )
        MemberRoleAssignment.objects.create(
            member=new_person,
            role=role
        )
        BranchRoleConfig.objects.create(
            role=role,
            role_display="Grand Marshall",
            hierarchy_tier=0,
            page=senate_member_page
        )
        if created: print(f"Created {name}")

        for vgm in ["Internal", "External"]:
            name = f"Vice Grand Marshall for {vgm} Affairs"
            role, created = Role.objects.update_or_create(
                name=name,
                defaults={
                    "name": name,
                    "positions": 1,
                    "constituency": 'none',
                }
            )
            new_person = self.make_person(class_choices()[0][0])
            MemberRoleAssignment.objects.create(
                member=new_person,
                role=role
            )
            BranchRoleConfig.objects.create(
                role=role,
                role_display=name,
                hierarchy_tier=1,
                page=senate_member_page
            )
            if created: print(f"Created {name}")

        name = f"FSL Senator"
        role, created = Role.objects.update_or_create(
            name=name,
            defaults={
                "name": name,
                "positions": 3,
                "constituency": 'associated',
            }
        )
        for i in range(3):
            new_person = self.make_person(class_choices()[0][0])
            MemberRoleAssignment.objects.create(
                member=new_person,
                role=role
            )
            senators_list.append(new_person)
        BranchRoleConfig.objects.create(
            role=role,
            role_display=name,
            hierarchy_tier=3,
            page=senate_member_page
        )
        if created: print(f"Created {name}")

        name = f"Independent Senator"
        role, created = Role.objects.update_or_create(
            name=name,
            defaults={
                "name": name,
                "positions": 3,
                "constituency": 'independent',
            }
        )
        for i in range(3):
            new_person = self.make_person(class_choices()[0][0])
            MemberRoleAssignment.objects.create(
                member=new_person,
                role=role
            )
            senators_list.append(new_person)
        BranchRoleConfig.objects.create(
            role=role,
            role_display=name,
            hierarchy_tier=3,
            page=senate_member_page
        )
        if created: print(f"Created {name}")

        for i in range(9):
            committee_name = self.gen_committee()
            name = f"{committee_name} Chair"
            role, created = Role.objects.update_or_create(
                name=name,
                defaults={
                    "name": name,
                    "positions": 1,
                    "constituency": 'none',
                }
            )
            new_person = self.make_person(class_choices()[0][0])
            MemberRoleAssignment.objects.create(
                member=new_person,
                role=role
            )
            BranchRoleConfig.objects.create(
                role=role,
                role_display=name,
                hierarchy_tier=2,
                page=senate_member_page
            )
            if created: print(f"Created {name}")

            committee_page = CommitteePage(
                title=committee_name,
                slug='_'.join(i.lower() for i in committee_name.split(" ")),
                show_in_menus=False,
                description=''.join([random.choice(string.ascii_lowercase+"                            .") for _ in range(1000)]),
                meeting_time=random.choice(["Monday", "Tuesday", "Wednesday", "Thursday"])+" "+str(random.choice([12,1,2,3,4,5,6]))+"pm",
                meeting_location=f"Union Room {''.join([str(random.choice(range(10))) for _ in range(4)])}"
            )
            
            senate_committee_page.add_child(instance=committee_page)

            CommitteeRoleConfig.objects.create(
                role=role,
                role_display="Chair",
                hierarchy_tier=0,
                page=committee_page
            )

            random_senator = random.choice(senators_list)

            CommitteeMemberPlacement.objects.create(
                page=committee_page,
                member=random_senator,
                committee_role="Vice Chair"
            )

            for i in range(5):
                random_senator = random.choice(senators_list)
    
                CommitteeMemberPlacement.objects.create(
                    page=committee_page,
                    member=random_senator,
                    committee_role="Member"
                )

        eboard_branch_page = BranchPage(
            branch_type="eboard",
            tagline="The E-Board branch of student government.",
            image=None,
            image_credit="",
            image_credit_url="",
            body=[],
            contact_email="pu@rpi.edu",
            meeting_schedule="",
            title="E-Board",
            slug="eboard",
            show_in_menus=True
        )

        root_page.add_child(instance=eboard_branch_page)

        eboard_member_page = MemberListingPage(
            title="E-Board Member List",
            slug="eboard_member_list",
            intro="The members of the E-Board.",
            show_in_menus=True
        )

        eboard_branch_page.add_child(instance=eboard_member_page)

        for officer_role in ["Secretary", "Treasurer", "Parlimenatarian"]:
            name = f"[E-Board] {officer_role}"
            role, created = Role.objects.update_or_create(
                name=name,
                defaults={
                    "name": name,
                    "positions": 1,
                    "constituency": 'none',
                }
            )
            new_person = self.make_person(class_choices()[0][0])
            MemberRoleAssignment.objects.create(
                member=new_person,
                role=role
            )
            BranchRoleConfig.objects.create(
                role=role,
                role_display=officer_role,
                hierarchy_tier=1,
                page=eboard_member_page
            )
            if created: print(f"Created {name}")

        name = f"President of the Union"
        role, created = Role.objects.update_or_create(
            name=name,
            defaults={
                "name": name,
                "positions": 1,
                "constituency": 'none',
            }
        )
        new_person = self.make_person(class_choices()[0][0])
        MemberProfile.objects.filter(email=new_person.email).update(
            first_name = "Alyssa P.",
            last_name = "Hacker",
            email = "hackea@rpi.edu"   
        )
        MemberRoleAssignment.objects.create(
            member=new_person,
            role=role
        )
        BranchRoleConfig.objects.create(
            role=role,
            role_display="President of the Union",
            hierarchy_tier=0,
            page=eboard_member_page
        )
        if created: print(f"Created {name}")

        for vp in ["Board Operations", "Club Relations", "Rules and Special Projects"]:
            name = f"Vice President for {vp}"
            role, created = Role.objects.update_or_create(
                name=name,
                defaults={
                    "name": name,
                    "positions": 1,
                    "constituency": 'none',
                }
            )
            new_person = self.make_person(class_choices()[0][0])
            MemberRoleAssignment.objects.create(
                member=new_person,
                role=role
            )
            BranchRoleConfig.objects.create(
                role=role,
                role_display=name,
                hierarchy_tier=1,
                page=eboard_member_page
            )
            if created: print(f"Created {name}")

        name = f"Club & Organization Representative"
        role, created = Role.objects.update_or_create(
            name=name,
            defaults={
                "name": name,
                "positions": 6,
                "constituency": 'none',
            }
        )
        for i in range(6):
            new_person = self.make_person(class_choices()[0][0])
            MemberRoleAssignment.objects.create(
                member=new_person,
                role=role
            )
        BranchRoleConfig.objects.create(
            role=role,
            role_display=name,
            hierarchy_tier=3,
            page=eboard_member_page
        )
        if created: print(f"Created {name}")

        name = f"Member-At-Large Representative"
        role, created = Role.objects.update_or_create(
            name=name,
            defaults={
                "name": name,
                "positions": 4,
                "constituency": 'none',
            }
        )
        for i in range(4):
            new_person = self.make_person(class_choices()[0][0])
            MemberRoleAssignment.objects.create(
                member=new_person,
                role=role
            )
        BranchRoleConfig.objects.create(
            role=role,
            role_display=name,
            hierarchy_tier=3,
            page=eboard_member_page
        )
        if created: print(f"Created {name}")

        for class_num, _ in class_choices():
            if class_num == "graduate": continue
            name = f"[E-Board] Class of {class_num} Representative"
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
            BranchRoleConfig.objects.create(
                role=role,
                role_display=f"Class of {class_num} Representative",
                hierarchy_tier=3,
                page=eboard_member_page
            )
            if created: print(f"Created {name}")


        eboard_committee_page = CommitteeIndexPage(
            title="E-Board Committeee List",
            slug="eboard_committee_list",
            intro="The committees of E-Board.",
            show_in_menus=True
        )

        eboard_branch_page.add_child(instance=eboard_committee_page)
            
        for i in range(9):
            committee_name = self.gen_committee()

            committee_page = CommitteePage(
                title=committee_name,
                slug='_'.join(i.lower() for i in committee_name.split(" ")),
                show_in_menus=False,
                description=''.join([random.choice(string.ascii_lowercase+"                            .") for _ in range(1000)]),
                meeting_time=random.choice(["Monday", "Tuesday", "Wednesday", "Thursday"])+" "+str(random.choice([12,1,2,3,4,5,6]))+"pm",
                meeting_location=f"Union Room {''.join([str(random.choice(range(10))) for _ in range(4)])}"
            )
            
            eboard_committee_page.add_child(instance=committee_page)

        SiteSettings.objects.update(
            box_archive_url="https://rpi.app.box.com/v/rpisg"
        )

        records_page = RecordIndexPage(
            title="Record",
            slug="the-record",
            intro="The records of student government.",
            show_in_menus=True
        )

        root_page.add_child(instance=records_page)

        complaint_form = ComplaintFormPage(
            title="Complaint Form",
            slug="complaint-form",
            intro="Submit a complaint to the government.",
            show_in_menus=True
        )

        root_page.add_child(instance=complaint_form)
        
        reps_form = RepsFormPage(
            title="Representative Finder",
            slug="reps-form",
            intro="Find your representatives!",
            show_in_menus=True
        )

        root_page.add_child(instance=reps_form)

    emails = ["bitdib@rpi.edu", "hackea@rpi.edu"]
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

    def gen_committee(self):
        out = ""
        for i in range(3):
            out += ''.join([random.choice(string.ascii_lowercase) for _ in range([7,3,7][i])]).capitalize() +" "
        return out + "Committee"
