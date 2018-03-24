from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import VehRestriction, DriverRestriction, LicenceCode, Ticket, TicketCategory, Severity,  Direction, Sex, \
    HairColor, EyesColor, ViolationCode, LicenceInfo, VehicleMake, Occupation, VehicleInfo
# Register your models here.

from .models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'


class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )

    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    list_select_related = ('profile', )



    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


class TicketCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'dateCreated', 'createdBy')
    list_filter = ('dateCreated', 'createdBy')

    fieldsets = [
        ('Ticket Type',
         {'fields': ('name', 'description'), }),
        ('Hidden Fields',
         {'fields': [('createdBy',)], 'classes': ['hidden']}),
    ]

    def get_changeform_initial_data(self, request):
        get_data = super(TicketCategoryAdmin, self).get_changeform_initial_data(request)
        get_data['createdBy'] = request.user.pk
        return get_data


admin.site.register(TicketCategory, TicketCategoryAdmin)


class SeverityAdmin(admin.ModelAdmin):

    list_display = ('name', 'dateCreated', 'createdBy')
    list_filter = ('dateCreated', 'createdBy')

    fieldsets = [
        ('Severities',
         {'fields': ('name',), }),
        ('Hidden Fields',
         {'fields': [('createdBy',)], 'classes': ['hidden']}),
    ]

    def get_changeform_initial_data(self, request):
        get_data = super(SeverityAdmin, self).get_changeform_initial_data(request)
        get_data['createdBy'] = request.user.pk
        return get_data


admin.site.register(Severity, SeverityAdmin)


class SexAdmin(admin.ModelAdmin):

    list_display = ('name', 'dateCreated', 'createdBy')
    list_filter = ('dateCreated', 'createdBy')

    fieldsets = [
        ('Sex (Gender)',
         {'fields': ('name',), }),
        ('Hidden Fields',
         {'fields': [('createdBy',)], 'classes': ['hidden']}),
    ]

    def get_changeform_initial_data(self, request):
        get_data = super(SexAdmin, self).get_changeform_initial_data(request)
        get_data['createdBy'] = request.user.pk
        return get_data


admin.site.register(Sex, SexAdmin)


class EyesColorAdmin(admin.ModelAdmin):

    list_display = ('name', 'dateCreated', 'createdBy')
    list_filter = ('dateCreated', 'createdBy')

    fieldsets = [
        ('Eyes Color',
         {'fields': ('name',), }),
        ('Hidden Fields',
         {'fields': [('createdBy',)], 'classes': ['hidden']}),
    ]

    def get_changeform_initial_data(self, request):
        get_data = super(EyesColorAdmin, self).get_changeform_initial_data(request)
        get_data['createdBy'] = request.user.pk
        return get_data


admin.site.register(EyesColor, EyesColorAdmin)


class LicenceInfoAdmin(admin.ModelAdmin):

    list_display = ('licenceNumber', 'licenceCode', 'licenceBarcode', 'idNumber', 'owner', 'issuedBy', 'validityStart', 'validityEnd',  'firstIssue')
    list_filter = ('dateCreated', 'driverRestriction', 'licenceCode', 'issuedBy', 'createdBy')

    fieldsets = [
        ('Licence information',
         {'fields': ('licenceNumber', 'licenceCode', 'licenceBarcode', 'idNumber', 'owner', 'driverRestriction', 'vehRestriction', 'issuedBy', 'validityStart', 'validityEnd', 'firstIssue',), }),
        ('Hidden Fields',
         {'fields': [('createdBy',)], 'classes': ['hidden']}),
    ]

    def get_changeform_initial_data(self, request):
        get_data = super(LicenceInfoAdmin, self).get_changeform_initial_data(request)
        get_data['createdBy'] = request.user.pk
        return get_data


admin.site.register(LicenceInfo, LicenceInfoAdmin)


class VehicleInfoAdmin(admin.ModelAdmin):

    list_display = ('regNumber', 'vinNumber', 'regBarcode', 'owner')
    list_filter = ('dateCreated', 'createdBy')

    fieldsets = [
        ('Vehicle information',
         {'fields': ('regNumber', 'vinNumber', 'regBarcode', 'owner',), }),
        ('Hidden Fields',
         {'fields': [('createdBy',)], 'classes': ['hidden']}),
    ]

    def get_changeform_initial_data(self, request):
        get_data = super(VehicleInfoAdmin, self).get_changeform_initial_data(request)
        get_data['createdBy'] = request.user.pk
        return get_data


admin.site.register(VehicleInfo, VehicleInfoAdmin)


class HairColorAdmin(admin.ModelAdmin):

    list_display = ('name', 'dateCreated', 'createdBy')
    list_filter = ('dateCreated', 'createdBy')

    fieldsets = [
        ('Hair Color',
         {'fields': ('name',), }),
        ('Hidden Fields',
         {'fields': [('createdBy',)], 'classes': ['hidden']}),
    ]

    def get_changeform_initial_data(self, request):
        get_data = super(HairColorAdmin, self).get_changeform_initial_data(request)
        get_data['createdBy'] = request.user.pk
        return get_data


admin.site.register(HairColor, HairColorAdmin)


class ViolationCodeAdmin(admin.ModelAdmin):

    list_display = ('code', 'amount', 'description', 'ticketCategory', 'dateCreated', 'createdBy')
    list_filter = ('dateCreated', 'ticketCategory', 'amount', 'createdBy')

    fieldsets = [
        ('Violation Code',
         {'fields': ('code', 'amount', 'ticketCategory', 'description',), }),
        ('Hidden Fields',
         {'fields': [('createdBy',)], 'classes': ['hidden']}),
    ]

    def get_changeform_initial_data(self, request):
        get_data = super(ViolationCodeAdmin, self).get_changeform_initial_data(request)
        get_data['createdBy'] = request.user.pk
        return get_data


admin.site.register(ViolationCode, ViolationCodeAdmin)


class LicenceCodeAdmin(admin.ModelAdmin):

    list_display = ('code', 'description', 'dateCreated', 'createdBy')
    list_filter = ('dateCreated', 'code', 'createdBy')

    fieldsets = [
        ('Licence Code',
         {'fields': ('code',  'description',), }),
        ('Hidden Fields',
         {'fields': [('createdBy',)], 'classes': ['hidden']}),
    ]

    def get_changeform_initial_data(self, request):
        get_data = super(LicenceCodeAdmin, self).get_changeform_initial_data(request)
        get_data['createdBy'] = request.user.pk
        return get_data


admin.site.register(LicenceCode, LicenceCodeAdmin)


class DriverRestrictionAdmin(admin.ModelAdmin):

    list_display = ('code', 'name', 'dateCreated', 'createdBy')
    list_filter = ('dateCreated', 'name', 'code', 'createdBy')

    fieldsets = [
        ('Driver Restriction',
         {'fields': ('code', 'name',), }),
        ('Hidden Fields',
         {'fields': [('createdBy',)], 'classes': ['hidden']}),
    ]

    def get_changeform_initial_data(self, request):
        get_data = super(DriverRestrictionAdmin, self).get_changeform_initial_data(request)
        get_data['createdBy'] = request.user.pk
        return get_data


admin.site.register(DriverRestriction, DriverRestrictionAdmin)


class VehRestrictionAdmin(admin.ModelAdmin):

    list_display = ('code', 'name', 'dateCreated', 'createdBy')
    list_filter = ('dateCreated', 'name', 'code', 'createdBy')

    fieldsets = [
        ('Vehicle Restriction',
         {'fields': ('code', 'name',), }),
        ('Hidden Fields',
         {'fields': [('createdBy',)], 'classes': ['hidden']}),
    ]

    def get_changeform_initial_data(self, request):
        get_data = super(VehRestrictionAdmin, self).get_changeform_initial_data(request)
        get_data['createdBy'] = request.user.pk
        return get_data


admin.site.register(VehRestriction, VehRestrictionAdmin)


class VehicleMakeAdmin(admin.ModelAdmin):

    list_display = ('name', 'dateCreated', 'createdBy')
    list_filter = ('dateCreated', 'createdBy')

    fieldsets = [
        ('Vehicle Make',
         {'fields': ('name',), }),
        ('Hidden Fields',
         {'fields': [('createdBy',)], 'classes': ['hidden']}),
    ]

    def get_changeform_initial_data(self, request):
        get_data = super(VehicleMakeAdmin, self).get_changeform_initial_data(request)
        get_data['createdBy'] = request.user.pk
        return get_data


admin.site.register(VehicleMake, VehicleMakeAdmin)


class DirectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'dateCreated', 'createdBy')
    list_filter = ('dateCreated', 'createdBy')

    fieldsets = [
        ('Direction',
         {'fields': ('name',), }),
        ('Hidden Fields',
         {'fields': [('createdBy',)], 'classes': ['hidden']}),
    ]

    def get_changeform_initial_data(self, request):
        get_data = super(DirectionAdmin, self).get_changeform_initial_data(request)
        get_data['createdBy'] = request.user.pk
        return get_data


class OccupationAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'dateCreated', 'createdBy')
    list_filter = ('dateCreated', 'createdBy')

    fieldsets = [
        ('Direction',
         {'fields': ('name', 'description'), }),
        ('Hidden Fields',
         {'fields': [('createdBy',)], 'classes': ['hidden']}),
    ]

    def get_changeform_initial_data(self, request):
        get_data = super(OccupationAdmin, self).get_changeform_initial_data(request)
        get_data['createdBy'] = request.user.pk
        return get_data


admin.site.register(Occupation, OccupationAdmin)


class TicketAdmin(admin.ModelAdmin):
    list_display = ('email', 'cellNumber', 'vinNumber', 'regNumber', 'description', 'speed', 'make', 'licenceBarcode', 'ticketCategory', 'amount', 'direction', 'officerBatch', 'sex')
    list_filter = ('dateCreated', 'officerBatch', 'sex', 'violationCode', 'direction', 'ticketCategory')

    fieldsets = [
        ('Ticket',
         {'fields': ('email', 'cellNumber', 'vinNumber', 'regNumber', 'description', 'speed', 'make', 'licenceBarcode', 'amount', 'idNumber', 'ticketCategory', 'direction', 'officerBatch', 'sex'), }),

    ]


admin.site.register(Ticket, TicketAdmin)




