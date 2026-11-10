            c1,c2=st.columns(2)
            with c1:
                weight=st.number_input(t('weight'),min_value=0.1,max_value=100000.0,value=50.0,step=1.0)
                if kind=='gold':
                    opts={'22K (91.6%)':.916,'18K (75%)':.75,'24K (99.9%)':.999}
                else:
                    opts={'999 (99.9%)':.999,'925 (92.5%)':.925,'800 (80%)':.8}
                purity=st.selectbox(t('purity'),list(opts))
            with c2:
                if kind == 'gold' and rates:
                    rate = rates[purity]
                    st.metric('Gold rate (INR/gram)' if st.session_state.lang=='en' else 'బంగారం ధర (₹/గ్రాము)', f'₹{rate:,.2f}')
                    st.caption(('Source timestamp: ' + str(updated_at)) if updated_at else ('Retrieved: ' + fetched_at))
                    st.caption('Indicative market quote, not a lender valuation.' if st.session_state.lang=='en' else 'ఇది మార్కెట్ సూచన ధర మాత్రమే; రుణదాత తుది మూల్యాంకనం కాదు.')
                elif kind == 'gold':
                    st.warning('Live gold rates unavailable. Enter a reference rate manually; it is NOT a live quote.' if st.session_state.lang=='en' else 'ప్రస్తుత బంగారం ధర అందుబాటులో లేదు. సూచన ధరను మీరే నమోదు చేయండి; ఇది ప్రత్యక్ష ధర కాదు.')
                    rate=st.number_input('Manual 24K reference rate (₹/gram)' if st.session_state.lang=='en' else '24K సూచన ధర (₹/గ్రాము)',min_value=1.0,value=7100.0,step=10.0)
                else:
                    rate=st.number_input(t('rate'),min_value=1.0,value=90.0,step=10.0)
                ltv=st.slider(t('ltv'),min_value=10,max_value=80,value=75,step=5)
            # API quotes already include purity; manual gold and silver rates are pure-metal reference rates.
            collateral=weight*(rate if kind=='gold' and rates else opts[purity]*rate)
            amount=collateral*ltv/100
            extras={'weight':weight,'purity':purity,'rate':rate,'ltv':ltv,
                    'rate_source':'goldprice.dev' if kind=='gold' and rates else 'manual illustrative input',
                    'rate_timestamp':updated_at or fetched_at if kind=='gold' and rates else None}
        else:
            c1,c2=st.columns(2)
            with c1:
                if kind=='mortgage':
                    prop=st.number_input(t('property'),min_value=100000,value=5000000,step=100000)
                    ltv=st.slider(t('ltv'),10,70,50,5)
                    amount=prop*ltv/100
                else:amount=float(st.number_input(t('requested'),min_value=10000,max_value=100000000,value=500000,step=10000))
            with c2:
                annual=st.number_input(t('annual'),min_value=0.0,max_value=50.0,value=12.0,step=.5)
                months=st.number_input(t('tenure'),min_value=1,max_value=360,value=36 if kind=='personal' else 180,step=1)
            monthly=annual/1200
            emi=amount/months if monthly==0 else amount*monthly*(1+monthly)**months/((1+monthly)**months-1)
            interest=emi*months-amount
            extras={'annual_rate':annual,'months':months}
            if kind=='mortgage':extras.update({'property_value':prop,'ltv':ltv})
        submitted=st.form_submit_button('🧮 '+t('calculate'),use_container_width=True,type='primary')
    if submitted:st.session_state[f'estimate_{kind}']={'amount':amount,'collateral':collateral if kind in ('gold','silver') else None,'emi':emi if kind not in ('gold','silver') else None,'interest':interest if kind not in ('gold','silver') else None,'extras':extras}
    estimate=st.session_state.get(f'estimate_{kind}')
    if estimate:
        st.markdown(f'<div class="result"><strong>{t("estimate")}</strong><h2>{currency(estimate["amount"])}</h2><small>{t("note")}</small></div>',unsafe_allow_html=True)
        if kind in ('gold','silver'):st.metric(t('collateral'),currency(estimate['collateral']))
        else:
            a,b=st.columns(2);a.metric(t('emi'),currency(estimate['emi']));b.metric(t('interest'),currency(estimate['interest']))
    else:st.info(t('no_data'))
    return estimate

def setting(name, default=''):
    value = os.getenv(name)
    if value:
        return value
    try:
        return str(st.secrets.get(name, default))
    except (FileNotFoundError, KeyError, AttributeError):
        return default

def enquiry(kind,estimate):
    st.markdown(f'<div class="section">✉️ {t("apply_heading")}</div>',unsafe_allow_html=True)
    with st.form(f'enquiry_{kind}'):
        a,b=st.columns(2)
        with a:
            name=st.text_input(t('full_name'),key=f'name_{kind}')
            phone=st.text_input(t('phone'),key=f'phone_{kind}',placeholder='10-digit mobile number')
            city=st.text_input(t('city'),key=f'city_{kind}')
        with b:
            email=st.text_input(t('email'),key=f'email_{kind}')
            state=st.selectbox(t('state'),['Telangana','Andhra Pradesh','Karnataka','Tamil Nadu','Maharashtra','Other'],key=f'state_{kind}')
        consent=st.checkbox(t('consent'),key=f'consent_{kind}')
        submit=st.form_submit_button(t('apply'),type='primary',use_container_width=True)
    if submit:
        errors=[]
        if len(name.strip())<2: errors.append('పూర్తి పేరును నమోదు చేయండి (కనీసం 2 అక్షరాలు).' if st.session_state.lang=='te' else 'Enter a valid full name (at least 2 characters).')
        if not re.fullmatch(r'[6-9]\d{9}',phone.strip()): errors.append('చెల్లని ఫోన్ నంబర్: 6, 7, 8 లేదా 9తో ప్రారంభమయ్యే 10 అంకెల నంబర్ ఇవ్వండి.' if st.session_state.lang=='te' else 'Invalid phone number: enter exactly 10 digits starting with 6, 7, 8 or 9.')
        if len(city.strip())<2: errors.append('సరైన నగరం పేరును నమోదు చేయండి.' if st.session_state.lang=='te' else 'Enter a valid city.')
        if email.strip() and not re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+',email.strip()): errors.append('చెల్లని ఇమెయిల్ చిరునామా.' if st.session_state.lang=='te' else 'Invalid email address.')
        if errors:
            for error in errors: st.error(error)
            return
        if not consent: st.warning(t('consent'));return
        number=re.sub(r'\D','',setting(f'MATRIX_{kind.upper()}_WHATSAPP_NUMBER') or setting('MATRIX_WHATSAPP_NUMBER'))
        if not number: st.warning(t('missing'));return
        if len(number)==10: number='91'+number
        if not re.fullmatch(r'91[6-9]\d{9}',number): st.error('Invalid business WhatsApp configuration.');return
        lines=['Matrix Finance loan enquiry',f'Loan: {WORDS["en"][kind]}',f'Name: {name}',f'Phone: +91 {phone}',f'City: {city}',f'State: {state}']
        if email:lines.append(f'Email: {email}')
        if estimate:lines.append(f'Indicative estimate: {currency(estimate["amount"])}')
        link=f'https://wa.me/{number}?text={quote(chr(10).join(lines))}'
        st.info('Message prepared for the relevant loan team. Press Send in WhatsApp to deliver it.')
        st.success(t('submitted'))
        st.link_button('💬 '+t('open_whatsapp'),link,use_container_width=True)

def loan_page(kind):
    top();hero(t(kind),t(kind+'_desc'),kind+'hero')
    if kind=='gold':st.info('💍 '+ ('Gold ornaments are valued according to weight, purity and an assumed pure-metal rate.' if st.session_state.lang=='en' else 'బంగారు ఆభరణాల బరువు, స్వచ్ఛత, ఊహించిన ధర ఆధారంగా అంచనా లెక్కించబడుతుంది.'))
    elif kind=='silver':st.info('🪙 '+('Silver collateral eligibility is subject to business policy and verification.' if st.session_state.lang=='en' else 'వెండి తాకట్టు అర్హత వ్యాపార విధానం మరియు ధృవీకరణపై ఆధారపడుతుంది.'))
    elif kind=='personal':st.info('💳 '+('Compare monthly EMI across loan amounts and tenures.' if st.session_state.lang=='en' else 'రుణ మొత్తం, కాలవ్యవధి ఆధారంగా నెలవారీ EMIని పోల్చండి.'))
    elif kind=='housing':st.info('🏡 '+('Plan long-term repayments for a home purchase.' if st.session_state.lang=='en' else 'ఇంటి కొనుగోలు కోసం దీర్ఘకాలిక EMIలను ప్లాన్ చేసుకోండి.'))
    else:st.info('🏢 '+('Explore indicative borrowing against property value.' if st.session_state.lang=='en' else 'ఆస్తి విలువ ఆధారంగా రుణ అంచనా తెలుసుకోండి.'))
    estimate=calculator(kind);enquiry(kind,estimate);foot()

def contact():
    top();hero(t('contact'),t('contact_desc'))
    st.markdown(f'<div class="section">{t("contact_phone")}</div>',unsafe_allow_html=True)
    number=setting('MATRIX_PUBLIC_PHONE','Not configured')
    st.write(number)
    st.markdown(f'<div class="section">{t("contact_address")}</div>',unsafe_allow_html=True)
    st.write(setting('MATRIX_BRANCH_ADDRESS','Not configured'))
    loan_type = st.selectbox('రుణ రకం' if st.session_state.lang=='te' else 'Loan type', ['gold','silver','personal','housing','mortgage'], format_func=lambda x: t(x))
    enquiry(loan_type,None)
    st.info(t('disclaimer'));foot()

PAGE_OBJECTS={'home':st.Page(home,title='Home',url_path='home',default=True)}
for key in ('gold','silver','personal','housing','mortgage'):
    PAGE_OBJECTS[key]=st.Page(lambda k=key:loan_page(k),title=key.title(),url_path=key)
PAGE_OBJECTS['contact']=st.Page(contact,title='Contact',url_path='contact')
def faq_page():
    top();hero('తరచుగా అడిగే ప్రశ్నలు' if st.session_state.lang=='te' else 'Frequently Asked Questions','మీ ప్రశ్నలకు సమాధానాలు' if st.session_state.lang=='te' else 'Answers to common questions about loan enquiries.');faq_section();foot()
PAGE_OBJECTS['faq']=st.Page(faq_page,title='FAQs',url_path='faq')
pg=st.navigation(list(PAGE_OBJECTS.values()),position='hidden')
pg.run()
