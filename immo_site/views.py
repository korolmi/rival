from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q
from django.conf import settings

from .models import ContentEl,CatalogEl,PhotoEl,TextLabel,OrderMsg,QuestHdr,QuestSect,Quest,QuestVar,AnsHdr,Answers,AnsCmts

def _getProjName ( lang ):
	""" имя проекта для главного меню """

	return "myFrench<span class='style-red'>.HOUSE</span>"

def make1Nav(lang):
	""" создает список, из которого в view будет формироваться верхнеуровневая навигация """
	m1l = []
	for p in ContentEl.objects.filter(el_level=1,el_lang=lang).exclude(el_is_draft=False).exclude(el_in_menu=False):
		url = "page"
		if p.el_templ_name:
			url = p.el_templ_name
		m1l.append((p.el_menu,p.el_slug,url))

	return m1l

def pageView(request,lang,slug):
	""" отрисовывает страницу с контентом """

	# КОСТЫЛЬ: нужно использовать язык

	# готовим меню первого уровня
	m1l = make1Nav(lang)

	# готовим меню второго уровня
	# m2l = []
	# for pp in ContentEl.objects.filter(el_slug=slug):	# находим корневой элемент для отрисовки меню второго уровня
	# 	break;
	# if pp.el_level==1:
	# 	for p in ContentEl.objects.filter(el_level=2,el_parent__el_slug=slug).exclude(el_is_draft=False,el_in_menu=False):
	# 		m2l.append((p.el_menu,p.el_slug))
	# else:
	# 	for p in ContentEl.objects.filter(el_level=2,el_parent_id=pp.el_parent_id).exclude(el_is_draft=False,el_in_menu=False):
	# 		m2l.append((p.el_menu,p.el_slug))

	# готовим список любимых объектов с первой фоткой
	ol = []
	for o in CatalogEl.objects.filter(cat_is_favorit=True,cat_lang=lang):
		ph = None	# КОСТЫЛЬ: заменить на кртинку не найденного объекта
		phList = PhotoEl.objects.filter(ph_obj_no=o.cat_obj_no)
		if len(phList)>0:
			ph = phList[0]
		ol.append((o,ph))

	# читаем собственно страницу
	pg = None
	for p in ContentEl.objects.filter(el_slug=slug,el_lang=lang):
		pg = p
		pg.el_body = pg.el_body.replace("..**..","")	# удаляем CUT
		mList = PhotoEl.objects.filter(ph_obj_no=p.el_slug, ph_is_page=True)
		break
	mainPage = (pg.id==pg.el_parent_id)

	# заменяем картинки 
	body = []
	for imgPart in pg.el_body.split("..IMG.."):
		img = imgPart.split("..NUM..")
		body.append(img[0])
		if len(img)>1:	# был рисунок
			imgInd = int(img[1])
			body.append('<img class="img-responsive" src="{0}">'.format(mList[imgInd].ph_file.url))
	pg.el_body = "".join(body)

	# готовим страницы второго уровня (для страниц первого уровня)
	p2l = []
	st = [ "gr", "br"]
	sInd = 1
	if pg.el_level==1:
		for pp in ContentEl.objects.filter(el_level=2,el_lang=lang,el_parent_id=pg.id).exclude(el_is_draft=False):
			ph = None
			tDet = None
			if pp.el_body.find("..**..")>0:
				pp.el_body = pp.el_body.split("..**..")[0]	# отдаем до CUT
				for t in TextLabel.objects.filter(tl_lang=lang,tl_category="details"):
					tDet = t.tl_text
					break
			phList = PhotoEl.objects.filter(ph_obj_no=pp.el_slug, ph_is_page=True)
			if len(phList)>0:
				ph = phList[0]
			p2l.append((pp,ph,st[sInd],tDet))
			if sInd==0:
				sInd = 1
			else:
				sInd = 0

	# читаем метки для страниц
	tLabs = {}
	for t in TextLabel.objects.filter(tl_lang=lang,tl_category="page"):
		tLabs[t.tl_name] = t.tl_text

	projName = _getProjName(lang)

	# разбираемся с данными запроса, если были
	formRes = None
	fLabs = {}
	if pg.el_as_html:
		if request.method == 'POST':
			if request.is_ajax():
				rMsg = "(success)"
				for t in TextLabel.objects.filter(tl_lang=lang,tl_category=(slug+"_good")):
					rMsg = t.tl_text
					break
				price = request.POST.get('price')
				ord_type = request.POST.get('serv')
				subj = request.POST.get('subj')
				cont_type = request.POST.get('ctype')
				cont = request.POST.get('cont')
				details = request.POST.get('descr')
				data = {"resMsg":rMsg.format(ord_type,subj,cont_type,cont)}
				ordMsg = OrderMsg.objects.create(
				    ord_type = ord_type,
				    ord_price = price,
    				ord_subj = subj,
    				ord_details = details,
    				ord_ctype = cont_type,
    				ord_lang = lang,
    				ord_cont = cont
				)
				ordMsg.save()
				return JsonResponse(data)
		else:	# заполняем форму данными по умолчанию
			# читаем метки и плейсхолдеры для формы
			for t in TextLabel.objects.filter(Q(tl_category=slug) | Q(tl_category='form_common'),tl_lang=lang):
				if t.tl_name in fLabs:
					if type(fLabs[t.tl_name])!=list:	# еще не список - инициализируем
						fLabs[t.tl_name] = [ fLabs[t.tl_name] ]
					fLabs[t.tl_name].append(t.tl_text)
				else:
					fLabs[t.tl_name] = t.tl_text

	context = { 'm1': m1l, 'lang': lang, 'slug': slug, 'pg': pg, 'proj': projName, 'fav': ol, 'p2l': p2l, 'mp': mainPage, 'ph': mList, 'tl': tLabs, 'flabs': fLabs, 'fres': formRes }
	if mainPage:
		return render ( request, 'immo_site/main_page.html', context )
	else:
		return render ( request, 'immo_site/content_page.html', context )

def questView(request,lang,slug,ans=0):
	""" отрисовывает страницу с анкетой """

	ans = int(ans)

	# читаем метки для элементов каталога
	tLabs = {}
	for t in TextLabel.objects.filter(tl_lang=lang,tl_category="quest"):
		tLabs[t.tl_name] = t.tl_text

	if request.method == 'POST':	# отдали страницу с результатами
		if request.is_ajax():
			cmts = request.POST.get('cmt').split('[')[1].split(']')[0]
			anss = request.POST.get('ans').split('[')[1].split(']')[0]
			qhid = request.POST.get('qhid')
			# сохраняем ответы на вопросы анкеты
			ansHdr = AnsHdr.objects.create(
				ah_pers = "test",
				ah_is_etalon = False,
				ah_quest_hdr_id = qhid )
			ansHdr.save()
			ansid = ansHdr.id
			totScore = 0
			corAnsHdrId = QuestHdr.objects.filter(id=AnsHdr.objects.filter(id=ansid)[0].ah_quest_hdr_id)[0].qh_ans_hdr_id
			qHdrId = QuestHdr.objects.filter(id=AnsHdr.objects.filter(id=ansid)[0].ah_quest_hdr_id)[0].id
			isCorrect = {}
			for a in anss.split(","):
				ans = Answers.objects.create(
					a_quest_id = a.split(":")[0].replace('"',''),
					a_quest_var_id = a.split(":")[1].replace('"',''),
					a_ans_hdr_id = ansid)
				ans.save()
				if corAnsHdrId is not None:
					# определяем правильность ответа
					isCorrect [ ans.a_quest_id ] = 0
					if str(QuestVar.objects.filter(id=Answers.objects.filter(a_quest_id=ans.a_quest_id,a_ans_hdr_id=corAnsHdrId)[0].a_quest_var_id)[0].id) == str(ans.a_quest_var_id):
						if isCorrect[ ans.a_quest_id ]==0:
							isCorrect[ ans.a_quest_id ] = 1
					else:
						isCorrect[ ans.a_quest_id ] = 2

			for c in cmts.split(","):
				cc = c.split(":")[1].replace('"','')
				if len(cc)>0:
					ansc = AnsCmts.objects.create(
						ac_quest_id = c.split(":")[0].replace('"',''),
						ac_cmt = cc,
						ac_ans_hdr_id = ansid)
					ansc.save()

			# формируем текст ответного сообщения
			# КОСТЫЛЬ: надо убрать все тексты в базу
			rMsg = ""
			wrAns = ""
			noAns = ""
			maxScore = 0
			if corAnsHdrId is not None:		# анкета для проверки знаний
				# суммируем баллы и формируем тексты неправильных ответов
				for q in isCorrect:
					if isCorrect[q]==1:
						totScore += Quest.objects.filter(id=q)[0].q_weight
					else:
						wrAns += "<li>{0}</li>".format(Quest.objects.filter(id=q)[0].q_subj)
				# считаем максимум баллов и перечисляем вопросы без ответов
				for q in Quest.objects.filter(q_quest_sect__qs_quest_hdr=qHdrId):
					maxScore += q.q_weight
					if str(q.id) not in isCorrect:
						noAns += "<li>{0}</li>".format(q.q_subj)
				rMsg += tLabs["total"].format(str(totScore), str(maxScore))
				if len(wrAns)>0:
					rMsg += tLabs["wrans"]
					rMsg += "<ul>" + wrAns + "</ul>"
				if len(noAns)>0:
					rMsg += tLabs["noans"]
					rMsg += "<ul>" + noAns + "</ul>"
				if len(wrAns)>0 or len(noAns)>0:
					rMsg += tLabs["corans"].format(lang,slug,corAnsHdrId) 
			else:
				rMsg += tLabs["thanks"]
 
			data = {"resMsg":rMsg}
			return JsonResponse(data)
	else:	# заполняем форму данными по умолчанию
		hSects = []
		# читаем анкету
		for qh in QuestHdr.objects.filter(qh_slug=slug,qh_lang=lang):
			qSects = []
			for qs in QuestSect.objects.filter(qs_quest_hdr_id=qh.id).order_by('qs_ord_no'):
				qQuests = []
				for q in Quest.objects.filter(q_quest_sect_id=qs.id).order_by('q_ord_no'):
					qVars = []
					for qv in QuestVar.objects.filter(qv_quest_id=q.id).order_by('qv_ord_no'):
						ava = False
						if ans>0: # анкета с ответами
							av = Answers.objects.filter(a_ans_hdr_id=ans,a_quest_id=q.id,a_quest_var_id=qv.id)
							if len(av)>0:
								ava = True
						qVars.append([qv,ava])
						if qv.qv_linked_sect_id is not None:	# надо спрятять секцию
							hSects.append([qv.id,qv.qv_linked_sect_id,qv.qv_hide_sect])
					ansCmt = ""
					if ans>0:	# анкета с ответами
						ac = AnsCmts.objects.filter(ac_ans_hdr_id=ans,ac_quest_id=q.id)
						if len(ac)>0:
							ansCmt = ac[0].ac_cmt
					qQuests.append([q,qVars,ansCmt])
				qSects.append([qs,qQuests])	

	context = { 'qh': qh, 'qs': qSects, 'lang': lang, 'slug': slug, 'hs': hSects, 'ans': ans, 'tl': tLabs }
	return render ( request, 'immo_site/quest_page.html', context )

def briefView(request,lang,slug):
	""" отрисовывает страницу с выдержкой из контента """

	# КОСТЫЛЬ: нужно использовать язык

	# готовим меню первого уровня
	m1l = make1Nav(lang)

	# читаем собственно страницу
	pg = None
	for p in ContentEl.objects.filter(el_slug=slug,el_lang=lang):
		pg = p
		mList = PhotoEl.objects.filter(ph_obj_no=p.el_slug, ph_is_page=True)
		pgph = mList[0]
		break

	# заменяем картинки 
	body = []
	for imgPart in pg.el_body.split("..IMG.."):
		img = imgPart.split("..NUM..")
		body.append(img[0])
		if len(img)>1:	# был рисунок
			imgInd = int(img[1])
			body.append('<img class="img-responsive" src="{0}">'.format(mList[imgInd].ph_file.url))
	pg.el_body = "".join(body)

	# готовим страницы второго уровня (для страниц первого уровня)
	p2l = []
	st = [ "gr", "br"]
	sInd = 1
	if pg.el_level==1:
		for pp in ContentEl.objects.filter(el_level=2,el_lang=lang,el_parent_id=pg.id).exclude(el_is_draft=False):
			ph = None
			citList = []
			if pp.el_body.find("level_1")>0:
				for  cc in pp.el_body.split("level_1")[1:]:
					citList.append(cc.split(">")[1].split("</span")[0])
			else:
				citList.append("(no level_1 found)")
			phList = PhotoEl.objects.filter(ph_obj_no=pp.el_slug, ph_is_page=True)
			if len(phList)>0:
				ph = phList[0]
			p2l.append((pp,ph,st[sInd],citList))
			if sInd==0:
				sInd = 1
			else:
				sInd = 0

	# читаем метки для страниц
	tLabs = {}
	for t in TextLabel.objects.filter(tl_lang=lang,tl_category="page"):
		tLabs[t.tl_name] = t.tl_text

	# читаем подробнее на языках
	for t in TextLabel.objects.filter(tl_lang=lang,tl_category="details"):
		tDet = t.tl_text
		break	

	projName = _getProjName(lang)
	context = { 'm1': m1l, 'lang': lang, 'slug': slug, 'pg': pg, 'pgph': pgph, 'proj': projName, 'p2l': p2l, 'ph': mList, 'tl': tLabs, "det": tDet }
	return render ( request, 'immo_site/brief_page.html', context )

def objIndex(request,lang):
	""" список объектов каталога без фильтрации """

	# готовим меню первого уровня
	m1l = []
	for p in ContentEl.objects.filter(el_level=1,el_lang=lang).exclude(el_is_draft=False).exclude(el_in_menu=False):
		m1l.append((p.el_menu,p.el_slug))

	# готовим список объектов с первой фоткой и стилем
	ol = []
	st = [ "gr", "br"]
	sInd = 0
	for o in CatalogEl.objects.filter(cat_lang=lang).exclude(cat_is_draft=False):
		ph = None
		phList = PhotoEl.objects.filter(ph_obj_no=o.cat_obj_no, ph_is_page=False)
		if len(phList)>0:
			ph = phList[0]
		ol.append((o,ph,st[sInd]))
		if sInd==0:
			sInd = 1
		else:
			sInd = 0

	# читаем страницу каталога
	pg = None
	for p in ContentEl.objects.filter(el_slug='cat',el_lang=lang):
		pg = p
		break

	# читаем метки для элементов каталога
	tLabs = {}
	for t in TextLabel.objects.filter(tl_lang=lang,tl_category="cat"):
		tLabs[t.tl_name] = t.tl_text

	projName = _getProjName(lang)
	context = { 'm1': m1l, 'lang': lang, 'ol': ol, 'proj': projName, 'pg': pg, 'tl': tLabs  }
	return render ( request, 'immo_site/obj_list_page.html', context )

def objView(request,lang,code):
	""" отрисовывает страницу с информацией об объекте """

	# КОСТЫЛЬ: нужно использовать язык

	# готовим меню первого уровня
	m1l = []
	for p in ContentEl.objects.filter(el_level=1,el_lang=lang).exclude(el_is_draft=False).exclude(el_in_menu=False):
		m1l.append((p.el_menu,p.el_slug))

	# готовим список любимых объектов с первой фоткой
	ol = []
	for o in CatalogEl.objects.filter(cat_is_favorit=True,cat_lang=lang):
		ph = None	# КОСТЫЛЬ: заменить на кртинку не найденного объекта
		phList = PhotoEl.objects.filter(ph_obj_no=o.cat_obj_no, ph_is_page=False)
		if len(phList)>0:
			ph = phList[0]
		ol.append((o,ph))

	# читаем собственно страницу
	pg = None
	for p in CatalogEl.objects.filter(cat_obj_no=code,cat_lang=lang):
		pg = p
		phList = PhotoEl.objects.filter(ph_obj_no=code, ph_is_page=False)
		break
	# готовим список про расположение
	locl = pg.cat_loc_descr.split(",")

	# читаем метки для элементов каталога
	tLabs = {}
	for t in TextLabel.objects.filter(tl_lang=lang,tl_category="cat"):
		tLabs[t.tl_name] = t.tl_text

	projName = _getProjName(lang)
	context = { 'm1': m1l, 'lang': lang, 'pg': pg, 'proj': projName, 'ph': phList, 'fav': ol,  'll': locl, 'tl': tLabs }
	return render ( request, 'immo_site/object_page.html', context )

