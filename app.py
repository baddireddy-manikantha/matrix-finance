import os, re
from urllib.parse import quote
import streamlit as st

st.set_page_config(page_title='Matrix Finance | Loans', page_icon='💠', layout='wide', initial_sidebar_state='collapsed')
NAVY='#08274e'; GOLD='#d9a531'
PAGES=['home','gold','silver','personal','housing','mortgage','contact']
WORDS={
'en':{
'home':'Home','gold':'Gold Loan','silver':'Silver Loan','personal':'Personal Loan','housing':'Home Loan','mortgage':'Mortgage Loan','contact':'Contact Us','language':'Language / భాష','tagline':'Your Trusted Financial Partner','apply':'Apply Now','calculate':'Calculate Estimate','your_details':'Your Details','full_name':'Full Name','phone':'Phone Number','email':'Email (optional)','city':'City','state':'State','weight':'Weight (grams)','purity':'Purity','rate':'Assumed pure metal rate per gram (₹)','ltv':'Illustrative loan-to-value (%)','requested':'Requested loan amount (₹)','annual':'Illustrative annual interest rate (%)','tenure':'Tenure (months)','property':'Estimated property value (₹)','estimate':'Indicative Loan Estimate','collateral':'Indicative Collateral Value','emi':'Estimated monthly EMI','interest':'Estimated total interest','consent':'I consent to share my details with Matrix Finance through WhatsApp for a loan enquiry.','open_whatsapp':'Open WhatsApp Enquiry','missing':'Set MATRIX_WHATSAPP_NUMBER to the business WhatsApp number to enable enquiries.','validation':'Enter your full name, a valid 10-digit Indian mobile number, and your city.','note':'Illustrative estimate only. Rates are editable assumptions, not live quotes. Final valuation, eligibility, approval and terms depend on verification and applicable rules.','intro':'Simple financial solutions, designed around your needs.','explore':'Explore Our Loan Products','start':'Find a loan that fits your plans','apply_heading':'Enquire About This Loan','calc_heading':'Loan Estimator','submitted':'Review the prefilled message in WhatsApp and press Send to submit your enquiry.','no_data':'Calculate an estimate above, then complete your enquiry.','how':'How it works','step1':'Choose your loan','step2':'Calculate an estimate','step3':'Send your enquiry','home_desc':'Gold, silver, personal, home and property-backed loans — all in one place.','contact_desc':'Talk to our team about the right loan for you.','contact_phone':'Business phone','contact_address':'Branch address','home_cta':'Explore loans','gold_desc':'Explore an indicative loan against eligible gold jewellery.','silver_desc':'Estimate borrowing against eligible silver collateral.','personal_desc':'Plan a personal loan with a simple monthly EMI estimate.','housing_desc':'Explore monthly payments for your dream home.','mortgage_desc':'Estimate a property-backed loan based on property value.','loan_info':'Loan Details','disclaimer':'We do not guarantee loan approval. Please confirm terms with Matrix Finance.'},
 'te':{
'home':'హోమ్','gold':'బంగారు రుణం','silver':'వెండి రుణం','personal':'వ్యక్తిగత రుణం','housing':'గృహ రుణం','mortgage':'తనఖా రుణం','contact':'సంప్రదించండి','language':'భాష / Language','tagline':'మీ విశ్వసనీయ ఆర్థిక భాగస్వామి','apply':'ఇప్పుడే దరఖాస్తు చేయండి','calculate':'అంచనా లెక్కించండి','your_details':'మీ వివరాలు','full_name':'పూర్తి పేరు','phone':'ఫోన్ నంబర్','email':'ఇమెయిల్ (ఐచ్ఛికం)','city':'నగరం','state':'రాష్ట్రం','weight':'బరువు (గ్రాములు)','purity':'స్వచ్ఛత','rate':'స్వచ్ఛమైన లోహం గ్రాము ఊహించిన ధర (₹)','ltv':'ఉదాహరణ రుణ విలువ నిష్పత్తి (%)','requested':'కావలసిన రుణ మొత్తం (₹)','annual':'ఉదాహరణ వార్షిక వడ్డీ రేటు (%)','tenure':'కాలవ్యవధి (నెలలు)','property':'ఆస్తి అంచనా విలువ (₹)','estimate':'రుణ మొత్తం అంచనా','collateral':'తాకట్టు అంచనా విలువ','emi':'నెలవారీ EMI అంచనా','interest':'మొత్తం వడ్డీ అంచనా','consent':'రుణ విచారణ కోసం నా వివరాలను వాట్సాప్ ద్వారా మ్యాట్రిక్స్ ఫైనాన్స్‌తో పంచుకోవడానికి అంగీకరిస్తున్నాను.','open_whatsapp':'వాట్సాప్ విచారణ తెరవండి','missing':'విచారణలను ప్రారంభించడానికి MATRIX_WHATSAPP_NUMBER లో వ్యాపార వాట్సాప్ నంబర్‌ను సెట్ చేయండి.','validation':'పూర్తి పేరు, సరైన 10 అంకెల భారతీయ మొబైల్ నంబర్ మరియు నగరం నమోదు చేయండి.','note':'ఇది కేవలం ఉదాహరణ అంచనా. ధరలు ప్రత్యక్ష మార్కెట్ ధరలు కావు. తుది విలువ, అర్హత, ఆమోదం మరియు షరతులు ధృవీకరణ, వర్తించే నియమాలపై ఆధారపడతాయి.','intro':'మీ అవసరాలకు అనుగుణంగా సులభమైన ఆర్థిక పరిష్కారాలు.','explore':'మా రుణ ఎంపికలు','start':'మీ ప్రణాళికలకు తగిన రుణాన్ని ఎంచుకోండి','apply_heading':'ఈ రుణం గురించి విచారించండి','calc_heading':'రుణ అంచనా కాలిక్యులేటర్','submitted':'వాట్సాప్‌లో ముందుగా నింపిన సందేశాన్ని చూసి, విచారణ పంపడానికి Send నొక్కండి.','no_data':'పైన అంచనా లెక్కించి, తరువాత విచారణ వివరాలు పూర్తి చేయండి.','how':'ఇది ఎలా పనిచేస్తుంది','step1':'రుణాన్ని ఎంచుకోండి','step2':'అంచనా లెక్కించండి','step3':'విచారణ పంపండి','home_desc':'బంగారు, వెండి, వ్యక్తిగత, గృహ మరియు ఆస్తి తనఖా రుణాలు — అన్నీ ఒకేచోట.','contact_desc':'మీకు సరిపోయే రుణం గురించి మా బృందాన్ని సంప్రదించండి.','contact_phone':'వ్యాపార ఫోన్','contact_address':'శాఖ చిరునామా','home_cta':'రుణాలను చూడండి','gold_desc':'అర్హత గల బంగారు ఆభరణాలపై రుణ అంచనా తెలుసుకోండి.','silver_desc':'అర్హత గల వెండి తాకట్టుపై రుణ అంచనా తెలుసుకోండి.','personal_desc':'సులభమైన నెలవారీ EMI అంచనాతో వ్యక్తిగత రుణాన్ని ప్లాన్ చేసుకోండి.','housing_desc':'మీ సొంత ఇంటి కోసం నెలవారీ EMI అంచనా చూడండి.','mortgage_desc':'ఆస్తి విలువ ఆధారంగా తనఖా రుణ అంచనా తెలుసుకోండి.','loan_info':'రుణ వివరాలు','disclaimer':'రుణ ఆమోదానికి హామీ లేదు. షరతులను మ్యాట్రిక్స్ ఫైనాన్స్‌తో నిర్ధారించుకోండి.'}}

st.markdown('''<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Noto+Sans+Telugu:wght@400;500;600;700&display=swap');
html,body,[class*="css"],.stApp{font-family:Inter,'Noto Sans Telugu',sans-serif!important}.stApp{background:#f7f9fc;color:#102d52}.block-container{max-width:1450px;padding-top:1rem;padding-bottom:4rem}header[data-testid="stHeader"]{background:transparent}
.brand{display:flex;gap:12px;align-items:center}.mark{font-size:40px;font-weight:900;background:linear-gradient(140deg,#fbe3a0,#b8790b);color:transparent;background-clip:text}.brandname{font-size:22px;font-weight:800;color:#08274e}.tagline{font-size:12px;color:#5b6c80}
.hero{padding:48px 42px;border-radius:22px;color:white;margin:22px 0 28px;min-height:200px;background:linear-gradient(110deg,#061d3b,#164b7c)}.hero h1{font-size:clamp(32px,4.2vw,53px);line-height:1.2;margin:0 0 12px;color:#f0c66c}.hero p{font-size:17px;max-width:700px;color:#e7edf6}.goldhero{background:linear-gradient(110deg,#071e3d,#164573 72%,#9a6b24)}.silverhero{background:linear-gradient(110deg,#112d48,#456782 72%,#8294a9)}.personalhero{background:linear-gradient(110deg,#08274e,#236c90)}.housinghero{background:linear-gradient(110deg,#08274e,#245a76 75%,#397b68)}.mortgagehero{background:linear-gradient(110deg,#08274e,#37446f 75%,#655c85)}
.tile{background:white;border:1px solid #e2e9f2;border-radius:17px;padding:24px;min-height:175px;box-shadow:0 7px 25px #08274e0a}.tile h3{font-size:20px;color:#08274e;margin:7px 0}.tile p{color:#64748b;font-size:14px}.tile .emoji{font-size:32px}.section{font-size:23px;font-weight:800;color:#08274e;margin:20px 0 14px}.result{border:1px solid #e8c476;border-radius:18px;padding:25px;background:linear-gradient(135deg,#fff8e8,#fff);margin:12px 0}.result h2{font-size:40px;color:#08274e;margin:6px 0}.result small{color:#64748b}.footer{margin-top:40px;padding:24px;border-radius:15px;background:#08274e;color:#e4eaf2;font-size:13px}
[data-testid="stForm"]{border:1px solid #e3e9f2;background:white;border-radius:18px;padding:18px;box-shadow:0 8px 28px #102d5210}
.stButton button[kind="primary"],div[data-testid="stFormSubmitButton"] button{background:linear-gradient(110deg,#08274e,#15538a);border:none;border-radius:11px;color:white;font-weight:700;min-height:47px}.stButton button[kind="secondary"]{background:#fff;border:1px solid #c79630;color:#08274e;border-radius:11px;min-height:45px;font-weight:700}
a[data-testid="stPageLink-NavLink"]{border-radius:10px;padding:7px 10px!important;font-weight:600}a[data-testid="stPageLink-NavLink"]:hover{background:#fff5dd}
@media(max-width:750px){.block-container{padding:1rem}.hero{padding:30px 22px;min-height:165px}.hero h1{font-size:30px}.hero p{font-size:14px}.brandname{font-size:18px}.mark{font-size:32px}.tile{min-height:135px;padding:16px}}
.float-hero{position:relative;overflow:hidden;min-height:270px;background:radial-gradient(circle at 75% 40%,#2c5b87,#08274e 65%);border-radius:22px;padding:45px 40px;margin:22px 0;color:white}.float-hero h1{font-size:clamp(30px,4vw,48px);max-width:580px;line-height:1.15;color:#f4c660}.float-hero p{max-width:500px;color:#e9eef6}.float-item{position:absolute;filter:drop-shadow(0 10px 12px #0006);animation:floaty 4s ease-in-out infinite}.float-item.one{right:20%;top:8%;font-size:90px}.float-item.two{right:4%;top:32%;font-size:90px;animation-delay:-1.3s}.float-item.three{right:33%;bottom:3%;font-size:70px;animation-delay:-2s}@keyframes floaty{0%,100%{transform:translateY(0)}50%{transform:translateY(-18px)}}@media(max-width:750px){.float-hero{padding:26px 20px 130px;min-height:340px}.float-item.one{right:55%;top:auto;bottom:5%;font-size:55px}.float-item.two{right:8%;top:auto;bottom:5%;font-size:65px}.float-item.three{right:35%;font-size:48px}}</style>''',unsafe_allow_html=True)

if 'lang' not in st.session_state:st.session_state.lang='en'
def t(key):return WORDS[st.session_state.lang][key]
def currency(n):return '₹'+format(round(n),',')
def top():
    a,b=st.columns([4,1.3],vertical_alignment='center')
    with a:st.markdown(f'<div class="brand"><div class="mark">M</div><div><div class="brandname">MATRIX FINANCE</div><div class="tagline">{t("tagline")}</div></div></div>',unsafe_allow_html=True)
    with b:st.selectbox('Language / భాష',['en','te'],format_func=lambda x:'English' if x=='en' else 'తెలుగు',key='lang',label_visibility='collapsed')
    with st.container(horizontal=True,horizontal_alignment='left'):
        for name in PAGES:st.page_link(PAGE_OBJECTS[name],label=t(name),icon={'home':'🏠','gold':'🥇','silver':'🪙','personal':'👤','housing':'🏡','mortgage':'🏢','contact':'☎️'}[name])

def hero(title,desc,theme=''):
    st.markdown(f'<div class="hero {theme}"><h1>{title}</h1><p>{desc}</p></div>',unsafe_allow_html=True)

def foot():st.markdown(f'<div class="footer">© Matrix Finance · {t("tagline")}<br>{t("disclaimer")}</div>',unsafe_allow_html=True)

def home():
    top()
    headline='Quick & Flexible Loans for Your Financial Needs' if st.session_state.lang=='en' else 'మీ ఆర్థిక అవసరాలకు సులభమైన రుణాలు'
    st.markdown(f'<div class="float-hero"><h1>{headline}</h1><p>{t("home_desc")}</p><span class="float-item one">💍</span><span class="float-item two">🏡</span><span class="float-item three">🪙</span></div>',unsafe_allow_html=True)
    st.markdown(f'<div class="section">{t("explore")}</div>',unsafe_allow_html=True)
    icons={'gold':'💍','silver':'🪙','personal':'💳','housing':'🏡','mortgage':'🏢'}
    for row in [['gold','silver','personal'],['housing','mortgage']]:
        cols=st.columns(3)
        for col,key in zip(cols,row):
            with col:
                st.markdown(f'<div class="tile"><div class="emoji">{icons[key]}</div><h3>{t(key)}</h3><p>{t(key+"_desc")}</p></div>',unsafe_allow_html=True)
                st.page_link(PAGE_OBJECTS[key],label=t('home_cta')+' →')
    st.markdown(f'<div class="section">{t("how")}</div>',unsafe_allow_html=True)
    for i,key in enumerate(['step1','step2','step3'],1):st.write(f'**{i}. {t(key)}**')
    foot()

def calculator(kind):
    st.markdown(f'<div class="section">🧮 {t("calc_heading")}</div>',unsafe_allow_html=True)
    with st.form(f'calc_{kind}'):
        if kind in ('gold','silver'):
            c1,c2=st.columns(2)
            with c1:
                weight=st.number_input(t('weight'),min_value=0.1,max_value=100000.0,value=50.0,step=1.0)
                if kind=='gold':opts={'22K (91.6%)':.916,'18K (75%)':.75,'24K (99.9%)':.999};base=7100.0
                else:opts={'999 (99.9%)':.999,'925 (92.5%)':.925,'800 (80%)':.8};base=90.0
                purity=st.selectbox(t('purity'),list(opts))
            with c2:
                rate=st.number_input(t('rate'),min_value=1.0,value=base,step=10.0)
                ltv=st.slider(t('ltv'),min_value=10,max_value=80,value=75,step=5)
            collateral=weight*opts[purity]*rate;amount=collateral*ltv/100
            extras={'weight':weight,'purity':purity,'rate':rate,'ltv':ltv}
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
        if len(name.strip())<2: errors.append('Enter a valid full name (at least 2 characters).')
        if not re.fullmatch(r'[6-9]\d{9}',phone.strip()): errors.append('Invalid phone number: enter exactly 10 digits starting with 6, 7, 8 or 9.')
        if len(city.strip())<2: errors.append('Enter a valid city.')
        if email.strip() and not re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+',email.strip()): errors.append('Invalid email address.')
        if errors:
            for error in errors: st.error(error)
            return
        if not consent: st.warning(t('consent'));return
        number=re.sub(r'\D','',os.getenv(f'MATRIX_{kind.upper()}_WHATSAPP_NUMBER','') or os.getenv('MATRIX_WHATSAPP_NUMBER','9441967571'))
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
    number=os.getenv('MATRIX_PUBLIC_PHONE','9441967571')
    st.write(number)
    st.markdown(f'<div class="section">{t("contact_address")}</div>',unsafe_allow_html=True)
    st.write(os.getenv('MATRIX_BRANCH_ADDRESS','Not configured'))
    st.info(t('disclaimer'));foot()

PAGE_OBJECTS={'home':st.Page(home,title='Home',url_path='home',default=True)}
for key in PAGES[1:-1]:PAGE_OBJECTS[key]=st.Page(lambda k=key:loan_page(k),title=key.title(),url_path=key)
PAGE_OBJECTS['contact']=st.Page(contact,title='Contact',url_path='contact')
pg=st.navigation(list(PAGE_OBJECTS.values()),position='hidden')
pg.run()
