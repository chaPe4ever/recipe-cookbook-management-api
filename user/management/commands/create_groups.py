from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


class Command(BaseCommand):
    help = "Create default user groups with permissions"

    def handle(self, *args, **kwargs):
        # Import your models
        from recipe.models import Recipe
        from cookbook.models import Cookbook
        from ingredient.models import Ingredient
        from author.models import Author
        from registration_profile.models import RegistrationProfile

        self.stdout.write("Creating groups...")

        # ========== 1. ADMINS GROUP ==========
        admins, created = Group.objects.get_or_create(name="Admins")
        if created:
            # Admins get all permissions
            all_permissions = Permission.objects.all()
            admins.permissions.set(all_permissions)
            self.stdout.write(
                self.style.SUCCESS('✓ Created "Admins" group with all permissions')
            )
        else:
            self.stdout.write(self.style.WARNING('- "Admins" group already exists'))

        # ========== 2. MODERATORS GROUP ==========
        moderators, created = Group.objects.get_or_create(name="Moderators")
        if created:
            # Moderators can do everything except delete users
            mod_permissions = Permission.objects.filter(
                content_type__app_label__in=[
                    "recipe",
                    "cookbook",
                    "ingredient",
                    "author",
                ]
            )
            moderators.permissions.set(mod_permissions)

            # Add view/change permissions for registration profiles
            reg_ct = ContentType.objects.get_for_model(RegistrationProfile)
            reg_perms = Permission.objects.filter(
                content_type=reg_ct,
                codename__in=["view_registrationprofile", "change_registrationprofile"],
            )
            moderators.permissions.add(*reg_perms)

            self.stdout.write(self.style.SUCCESS('✓ Created "Moderators" group'))
        else:
            self.stdout.write(self.style.WARNING('- "Moderators" group already exists'))

        # ========== 3. AUTHORS GROUP ==========
        authors, created = Group.objects.get_or_create(name="Authors")
        if created:
            # Authors can create/edit their own content
            author_permissions = []

            # Recipe permissions
            recipe_ct = ContentType.objects.get_for_model(Recipe)
            recipe_perms = Permission.objects.filter(
                content_type=recipe_ct,
                codename__in=[
                    "add_recipe",
                    "change_recipe",
                    "view_recipe",
                    "delete_recipe",
                ],
            )
            author_permissions.extend(recipe_perms)

            # Cookbook permissions
            cookbook_ct = ContentType.objects.get_for_model(Cookbook)
            cookbook_perms = Permission.objects.filter(
                content_type=cookbook_ct,
                codename__in=[
                    "add_cookbook",
                    "change_cookbook",
                    "view_cookbook",
                    "delete_cookbook",
                ],
            )
            author_permissions.extend(cookbook_perms)

            # Ingredient permissions (view and add only)
            ingredient_ct = ContentType.objects.get_for_model(Ingredient)
            ingredient_perms = Permission.objects.filter(
                content_type=ingredient_ct,
                codename__in=["add_ingredient", "view_ingredient"],
            )
            author_permissions.extend(ingredient_perms)

            # Author profile permissions
            author_ct = ContentType.objects.get_for_model(Author)
            author_prof_perms = Permission.objects.filter(
                content_type=author_ct, codename__in=["view_author", "change_author"]
            )
            author_permissions.extend(author_prof_perms)

            authors.permissions.set(author_permissions)
            self.stdout.write(self.style.SUCCESS('✓ Created "Authors" group'))
        else:
            self.stdout.write(self.style.WARNING('- "Authors" group already exists'))

        # ========== 4. EDITORS GROUP ==========
        editors, created = Group.objects.get_or_create(name="Editors")
        if created:
            # Editors can edit existing content but not delete
            editor_permissions = []

            for model in [Recipe, Cookbook, Ingredient]:
                ct = ContentType.objects.get_for_model(model)
                perms = Permission.objects.filter(
                    content_type=ct,
                    codename__in=[
                        f"view_{model._meta.model_name}",
                        f"change_{model._meta.model_name}",
                    ],
                )
                editor_permissions.extend(perms)

            editors.permissions.set(editor_permissions)
            self.stdout.write(self.style.SUCCESS('✓ Created "Editors" group'))
        else:
            self.stdout.write(self.style.WARNING('- "Editors" group already exists'))

        # ========== 5. VIEWERS GROUP ==========
        viewers, created = Group.objects.get_or_create(name="Viewers")
        if created:
            # Viewers can only view content (read-only)
            viewer_permissions = Permission.objects.filter(codename__startswith="view_")
            viewers.permissions.set(viewer_permissions)
            self.stdout.write(self.style.SUCCESS('✓ Created "Viewers" group'))
        else:
            self.stdout.write(self.style.WARNING('- "Viewers" group already exists'))

        self.stdout.write(self.style.SUCCESS("\n✓ All groups created successfully!"))
