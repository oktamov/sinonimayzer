from django.contrib import admin
from .models import Type, Method, Word, Synonym, Addition, AdditionType, BuildWord
from django.db import models
from django.urls import reverse
from django.forms import TextInput
from django.utils.html import format_html
from operator import or_
from django.db.models import Q

# Register your models here.


class AdditionTypeAdmin(admin.ModelAdmin):
    list_display = ['name']
    ordering = ['order', 'id']

class SynonymAdmin(admin.ModelAdmin):
    list_display = ['edit_link', 'w2', 'similar']
    search_fields = ['w1__s__startswith']
    list_filter = ['similar']
    ordering = ['w1', 'w2']

    def edit_link(self, obj):
        return format_html('<a href="{}">{}</a>', reverse('admin:synonym_word_change', args=(obj.w1.id,)), obj.w1)

    def get_search_results(self, request, queryset, search_term):
        queryset, may_have_duplicates = super().get_search_results(request, queryset, search_term,)
        try:
            search_term_as_int = int(search_term)
        except ValueError:
            pass
        else:
            queryset |= self.model.objects.filter(w1=search_term_as_int)
        return queryset, may_have_duplicates

    edit_link.short_description = "Word"

class AdditionAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'add', 'exeption']
    search_fields = ['name', 'add']
    list_filter = ['type']
    ordering = ['type', 'id']
    filter_horizontal = ['additions']
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'80'})},
    }


class WordAdmin(admin.ModelAdmin):
    list_display = ['word_name', 'type', 'method']
    search_fields = ['s']
    list_filter = ['type', 'method']
    ordering = ['id']
    #filter_horizontal = ['synonyms', 'additions']

    def word_name(self, obj):
        return obj.s

    def get_synonyms(self, obj):

        words = Synonym.objects.filter(w1=obj)
        ret = ''
        #for word in obj.synonyms.all():
        #    ret += '<a href="/admin/synonym/word/{}/change/"><b>{}</b></a><br>' . format(word.id, word)

        for word in words:
            ret += '<a href="/admin/synonym/word/{}/change/"><b>{}</b></a><br>' . format(word.w2.id, word.w2)
        return format_html(ret)

    word_name.short_description = 'Word'
    word_name.admin_order_field = 's'

    #get_synonyms.short_description = 'Synonyms'
    #get_synonyms.admin_order_field = 'synonyms'

class TypeAdmin(admin.ModelAdmin):
    list_display = ['name']
    filter_horizontal = ['additions']

class BuildWordAdmin(admin.ModelAdmin):
    list_display = ['word', 'root']


    def info(self, obj):
        res = obj.word

        if obj.additions != '':
            additions = obj.additions.split('-')
            for add in additions:
                addition = Addition.objects.get(id=int(add))
                if addition != None:
                    res += ' ' + str(addition)

        return res

    info.short_description = 'Info'
    info.admin_order_field = 'additions'


admin.site.register(Type, TypeAdmin)
admin.site.register(Method)
admin.site.register(AdditionType, AdditionTypeAdmin)
admin.site.register(Word, WordAdmin)
admin.site.register(Addition, AdditionAdmin)
admin.site.register(BuildWord, BuildWordAdmin)

admin.site.register(Synonym, SynonymAdmin)

#tt