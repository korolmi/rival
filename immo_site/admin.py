from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import ContentEl,CatalogEl,PhotoEl,TextLabel,PageTag,ShortContentEl,OrderMsg,QuestHdr,QuestSect,Quest,QuestVar,AnsHdr,Answers,AnsCmts

admin.site.register(PageTag)
admin.site.register(CatalogEl)
admin.site.register(PhotoEl)
admin.site.register(QuestHdr)

class ContentAdmin ( ImportExportModelAdmin ):

	list_display = ( 'id', 'el_level', 'el_lang', 'el_ord_no', 'el_slug', 'el_title', 'el_parent')
	list_filter = [ 'el_level', 'el_lang', ('el_parent',admin.RelatedOnlyFieldListFilter) ]
	search_fields = [ 'el_title', 'id' ]
	filter_horizontal = ("el_tags",)

	def formfield_for_foreignkey(self, db_field, request, **kwargs):
		if db_field.name == "el_parent":
			kwargs["queryset"] = ContentEl.objects.filter(el_level=1)
		return super(ContentAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

class ShortContentAdmin ( admin.ModelAdmin ):

	class Media: 
		js = ( 'jquery.js',
			'codemirror/codemirror.js',
			'codemirror/closebrackets.js',
			'codemirror/closetag.js',
			'codemirror/css.js',
			'codemirror/fullscreen.js',
			'codemirror/htmlmixed.js',
			'codemirror/javascript.js',
			'codemirror/matchbrackets.js',
			'codemirror/matchtags.js',
			'codemirror/xml-fold.js',
			'codemirror/xml.js',
			'cdmr_conf.js',)
		css = {
			'all' : ('codemirror/codemirror.css', 'codemirror/fullscreen.css', 'codemirror/cobalt.css')
		}

	list_display = ( 'id', 'el_level', 'el_lang', 'el_ord_no', 'el_slug', 'el_title', 'el_parent')
	list_filter = [ 'el_level', 'el_lang', ('el_parent',admin.RelatedOnlyFieldListFilter) ]
	search_fields = [ 'el_title', 'id' ]
	filter_horizontal = ("el_tags",)
	exclude = ["el_parent", "el_level", "el_ord_no", "el_lang", "el_meta_title", "el_meta_kwords", "el_type", "el_cre_date", "el_as_html", "el_templ_name", "el_page_color"]

class LabelAdmin ( ImportExportModelAdmin ):

	list_display = ( 'id', 'tl_lang', 'tl_category', 'tl_name', 'tl_text')
	list_filter = [ 'tl_category', 'tl_lang' ]
	search_fields = [ 'tl_text', 'tl_name' ]

class OrderAdmin ( admin.ModelAdmin ):

	list_display = ( 'id', 'ord_cre_date', 'ord_type', 'ord_subj', 'ord_cont', 'ord_lang')
	list_filter = [ 'ord_type', 'ord_lang' ]
	search_fields = [ 'ord_cont', 'ord_subj', 'ord_details' ]

class QuestAdmin ( admin.ModelAdmin ):

	list_display = ( 'id', 'q_ord_no', 'q_weight', 'q_subj', 'q_quest_sect')
	list_filter = [ 'q_quest_sect' ]
	search_fields = [ 'q_subj', 'q_details' ]

class QuestSectAdmin ( admin.ModelAdmin ):

	list_display = ( 'id', 'qs_ord_no', 'qs_quest_hdr', 'qs_subj')
	list_filter = [ 'qs_quest_hdr' ]
	search_fields = [ 'qs_subj', 'qs_details' ]

class QuestVarAdmin ( admin.ModelAdmin ):

	list_display = ( 'id', 'qv_ord_no', 'qv_quest', 'qv_ans')
	list_filter = [ 'qv_quest' ]
	search_fields = [ 'qv_quest', 'qv_ans' ]

class AnsHdrAdmin ( admin.ModelAdmin ):

	list_display = ( 'id', 'ah_pers', 'ah_cre_date', 'ah_is_etalon', 'ah_quest_hdr')
	list_filter = [ 'ah_quest_hdr' ]
	search_fields = [ 'ah_pers' ]

class AnswersAdmin ( admin.ModelAdmin ):

	list_display = ( 'id', 'a_ans_hdr', 'a_quest', 'a_quest_var' )
	list_filter = [ 'a_ans_hdr', 'a_quest' ]
	search_fields = [ 'a_quest' ]

class AnsCmtsAdmin ( admin.ModelAdmin ):

	list_display = ( 'id', 'ac_ans_hdr', 'ac_quest', 'ac_cmt' )
	list_filter = [ 'ac_ans_hdr', 'ac_quest' ]
	search_fields = [ 'ac_cmt' ]

admin.site.register(ContentEl,ContentAdmin)
admin.site.register(ShortContentEl,ShortContentAdmin)
admin.site.register(TextLabel,LabelAdmin)
admin.site.register(OrderMsg,OrderAdmin)
admin.site.register(Quest,QuestAdmin)
admin.site.register(QuestSect,QuestSectAdmin)
admin.site.register(QuestVar,QuestVarAdmin)
admin.site.register(AnsHdr,AnsHdrAdmin)
admin.site.register(Answers,AnswersAdmin)
admin.site.register(AnsCmts,AnsCmtsAdmin)

# EXPORT IMPORT
class TextLabResource(resources.ModelResource):

    class Meta:
        model = TextLabel
