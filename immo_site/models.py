from django.db import models

# константы для выбора языка
C_langs = (("en","EN"),("fr","FR"),("ru","RU"))

# константы для выбора типа контента
C_el_types = ((1,"Страница"),(2,"Ссылка"))

# справочник тэгов страниц
class PageTag(models.Model):

    tg_name = models.CharField('тэг',max_length=30)

    class Meta:
        verbose_name = "Тэг страниц"
        verbose_name_plural = "05. Тэги страниц"

    def __str__(self):              
        return self.tg_name

# элемент контента сайта (страница)
class ContentEl(models.Model):

    el_body = models.TextField('тело',max_length=100000,blank=True)
    el_parent = models.ForeignKey('self', null=True, blank=True, verbose_name='Родитель')
    el_level = models.IntegerField('Уровень',default=1)
    el_ord_no = models.IntegerField('Порядок',default=100)
    el_lang = models.CharField('язык',max_length=2,choices=C_langs,default="ru")
    el_meta_title = models.CharField('META title',max_length=1000,blank=True)
    el_meta_kwords = models.CharField('META kwords',max_length=1000,blank=True)
    el_menu = models.CharField('меню',max_length=100,blank=True)
    el_type = models.IntegerField('тип',choices=C_el_types,default=1)
    el_cre_date = models.DateField('дата',auto_now_add=True)
    el_slug = models.SlugField('slug',max_length=1000)
    el_title = models.CharField('заголовок',max_length=1000)
    el_is_draft = models.BooleanField('публикация',default=False)
    el_in_menu = models.BooleanField('в меню',default=False)
    el_as_html = models.BooleanField('в HTML',default=False)
    el_templ_name = models.CharField('шаблон',max_length=1000,blank=True)	# на самом деле сюда пишем часть урла: если заполнено, то она используется между языком и slugом
    el_page_color = models.CharField('цвет',max_length=100,blank=True)
    el_tags = models.ManyToManyField(PageTag, blank=True, verbose_name='Тэги')

    class Meta:
        verbose_name = "Элемент сайта (полный)"
        verbose_name_plural = "01. Элементы сайта (полные)"
        ordering = [ "el_ord_no" ]

    def __str__(self):              
        return self.el_title

class ShortContentEl(ContentEl):
    class Meta:
        verbose_name = "Страница"
        verbose_name_plural = "02. Страницы"
        ordering = [ "el_ord_no" ]
        proxy = True

# элемент каталога сайта 
class CatalogEl(models.Model):

	cat_parent = models.ForeignKey('ContentEl')
	cat_ord_no = models.IntegerField('порядок показа',default=100)    
	cat_obj_no = models.IntegerField('уникальный номер объекта',default=100)
	cat_lang = models.CharField('язык',max_length=2,choices=C_langs,default="ru")
	cat_meta_title = models.CharField('META заголовок страницы',max_length=1000,blank=True)
	cat_meta_kwords = models.CharField('META ключевые слова',max_length=1000,blank=True)
	cat_title = models.CharField('наименование объекта',max_length=1000)
	cat_sdescr = models.CharField('краткое описание',max_length=1000)
	cat_fdescr = models.TextField('подробное описание',max_length=10000,blank=True)
	cat_geo_x = models.CharField('координата Х',max_length=100,blank=True)
	cat_geo_y = models.CharField('координата Y',max_length=100,blank=True)
	cat_loc_name = models.CharField('имя местоположения',max_length=1000,blank=True)
	cat_loc_descr = models.CharField('описание местоположения',max_length=1000,blank=True)
	cat_price = models.IntegerField('цена EURO',default=1)
	cat_rooms = models.IntegerField('количество комнат',default=1)
	cat_srooms = models.IntegerField('количество спален',default=1)
	cat_brooms = models.IntegerField('количество ванных комнат',default=1)
	cat_floors = models.IntegerField('этажность',default=1)
	cat_fl_area = models.IntegerField('общая площадь дома в кв.метрах',default=1)
	cat_gr_area = models.IntegerField('общая площать участка',default=1)
	cat_constr_yr = models.CharField('год постройки и связанное',max_length=1000,blank=True)
	cat_page_color = models.CharField('цвет отображения (hex)',max_length=6,blank=True)
	cat_is_draft = models.BooleanField('признак готовности к публикации',default=False)
	cat_is_favorit = models.BooleanField('любимый объект',default=False)

	class Meta:
	    verbose_name = "Объект каталога"
	    verbose_name_plural = "06. Объекты каталога"
	    ordering = [ "cat_ord_no" ]

	def __str__(self):              
	    return self.cat_title

# фотография объекта
class PhotoEl(models.Model):

	ph_ord_no = models.IntegerField('порядок показа',default=100)    
	ph_obj_no = models.CharField('номер объекта или slug страницы',max_length=100)    
	ph_is_page = models.BooleanField('фотка со страницы',default=False)
	ph_descr = models.CharField('краткое описание',max_length=1000)
	ph_file =  models.ImageField('файл с фотографией')

	class Meta:
	    verbose_name = "Фото объекта"
	    verbose_name_plural = "04. Фото объекта"
	    ordering = [ "ph_ord_no" ]

	def __str__(self):              
	    return self.ph_descr

# текстовые метки для страниц
class TextLabel(models.Model):

	tl_lang = models.CharField('язык',max_length=2,choices=C_langs,default="ru")
	tl_category = models.CharField('категория метки',max_length=1000)
	tl_name = models.CharField('имя метки',max_length=1000)
	tl_text = models.CharField('текст метки',max_length=1000)

	class Meta:
	    verbose_name = "Текстовая метка"
	    verbose_name_plural = "03. Текстовые метки"
	    ordering = [ "tl_name" ]

	def __str__(self):              
	    return self.tl_text

# обращение от посетителя сайта (заказ услуги)
class OrderMsg(models.Model):

	ord_lang = models.CharField('язык',max_length=2,choices=C_langs,default="ru")
	ord_cre_date = models.DateTimeField('дата',auto_now_add=True)
	ord_type = models.CharField('тип',max_length=1000,blank=True)
	ord_subj = models.CharField('кратко',max_length=1000,blank=True)
	ord_details = models.TextField('детали',max_length=100000,blank=True)
	ord_ctype = models.CharField('конт тип',max_length=1000,blank=True)
	ord_cont = models.CharField('контакты',max_length=1000,blank=True)
	ord_price = models.CharField('цена',max_length=1000,blank=True)

	class Meta:
	    verbose_name = "Заказ услуги"
	    verbose_name_plural = "07. Заказы услуги"
	    ordering = [ "ord_cre_date" ]

	def __str__(self):              
	    return self.ord_subj

# анкета - шапка
class QuestHdr(models.Model):

	qh_lang = models.CharField('язык',max_length=2,choices=C_langs,default="ru")
	qh_cre_date = models.DateTimeField('дата',auto_now_add=True)
	qh_slug = models.CharField('slug',max_length=1000)
	qh_subj = models.CharField('кратко',max_length=1000)
	qh_details = models.TextField('детали',max_length=100000,blank=True)
	qh_ans_hdr = models.ForeignKey('AnsHdr',verbose_name='правильный ответ',on_delete=models.PROTECT,null=True,blank=True)


	class Meta:
	    verbose_name = "Заголовок анкеты"
	    verbose_name_plural = "08. Заголовки анкет"
	    ordering = [ "qh_cre_date" ]

	def __str__(self):              
	    return self.qh_subj

# секция анкеты
class QuestSect(models.Model):

	qs_ord_no = models.IntegerField('порядок показа',default=100)    
	qs_subj = models.CharField('кратко',max_length=1000,blank=True)
	qs_details = models.TextField('детали',max_length=100000,blank=True)
	qs_quest_hdr = models.ForeignKey(QuestHdr, on_delete=models.PROTECT)

	class Meta:
	    verbose_name = "Секция анкеты"
	    verbose_name_plural = "09. Секции анкет"
	    ordering = [ "qs_ord_no" ]

	def __str__(self):              
	    return self.qs_subj

# вопрос анкеты
class Quest(models.Model):

	q_ord_no = models.IntegerField('порядок показа',default=100)    
	q_weight = models.IntegerField('баллы',default=100)    
	q_subj = models.CharField('кратко',max_length=1000,blank=True)
	q_details = models.TextField('детали',max_length=100000,blank=True)
	q_quest_sect = models.ForeignKey(QuestSect, on_delete=models.PROTECT)
	q_need_single = models.BooleanField('требует один ответ',default=True)
	q_has_comment = models.BooleanField('допускает комментарий',default=True)
	q_show_as_list = models.BooleanField('показывать в виде списка',default=False)
	q_line_break = models.BooleanField('перенос строки после вопроса',default=False)
	q_quest_wd = models.CharField('ширина вопроса',max_length=1000,blank=True, default="col-md-6")
	q_cmt_wd = models.CharField('ширина коммента',max_length=1000,blank=True, default="col-md-6")
	q_ans_wd = models.CharField('ширина ответа',max_length=1000,blank=True, default="col-md-6")


	class Meta:
	    verbose_name = "Вопрос анкеты"
	    verbose_name_plural = "10. Вопросы анкет"
	    ordering = [ "q_ord_no" ]

	def __str__(self):              
	    return self.q_subj

# вариант ответа на вопрос анкеты
class QuestVar(models.Model):

	qv_ord_no = models.IntegerField('порядок показа',default=100)    
	qv_ans = models.CharField('кратко',max_length=1000,blank=True)
	qv_quest = models.ForeignKey(Quest, on_delete=models.PROTECT)
	qv_hide_sect = models.BooleanField('скрывать секцию',default=True)
	qv_linked_sect = models.ForeignKey(QuestSect, null=True, on_delete=models.SET_NULL,blank=True)

	class Meta:
	    verbose_name = "Вариант ответа на вопрос"
	    verbose_name_plural = "11. Варианты ответа на вопросы"
	    ordering = [ "qv_ord_no" ]

	def __str__(self):              
	    return self.qv_ans

# заголовок заполненной анкеты
class AnsHdr(models.Model):

	ah_pers = models.CharField('кто',max_length=1000,blank=True)
	ah_cre_date = models.DateTimeField('дата',auto_now_add=True)
	ah_is_etalon = models.BooleanField('правильный ответ',default=True)	
	ah_quest_hdr = models.ForeignKey(QuestHdr, on_delete=models.PROTECT)

	class Meta:

	    verbose_name = "Заголовок результата"
	    verbose_name_plural = "12. Заголовки результатов"
	    ordering = [ "ah_cre_date" ]

	def __str__(self):              
	    return self.ah_pers

# ответы на вопросы  анкеты
class Answers(models.Model):

	a_quest = models.ForeignKey(Quest, on_delete=models.PROTECT)
	a_quest_var = models.ForeignKey(QuestVar, on_delete=models.PROTECT)
	a_ans_hdr = models.ForeignKey(AnsHdr)

	class Meta:

	    verbose_name = "Ответ на вопрос"
	    verbose_name_plural = "13. Ответы на вопросы"
	    ordering = [ "a_quest_var" ]

	def __str__(self):              
	    return str(self.a_quest_var)

# комментарии к ответам на вопросы  анкеты
class AnsCmts(models.Model):

	ac_quest = models.ForeignKey(Quest, on_delete=models.PROTECT)
	ac_ans_hdr = models.ForeignKey(AnsHdr)
	ac_cmt = models.CharField('комментарий',max_length=1000,blank=True)

	class Meta:

	    verbose_name = "Комментарий к ответу"
	    verbose_name_plural = "14. Комментарии к ответам"
	    ordering = [ "ac_quest" ]

	def __str__(self):              
	    return str(self.ac_quest)
