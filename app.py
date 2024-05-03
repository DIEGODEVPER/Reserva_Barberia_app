import streamlit as st
from  streamlit_option_menu import option_menu
from google_calendar_class import GoogleCalendar
import numpy as np
import datetime as dt
import pytz as pytz
#import json as json
#import '..streamlit/secrets.toml' 
from send_email import send
#from google_sheets import GoogleSheet

#Funciones
def add_30_minutes(time_str):
    time_format = "%H:%M"
    parsed_time = dt.datetime.strptime(time_str, time_format).time()

    # Convert the time to a datetime object for easier manipulation
    time_datetime = dt.datetime.combine(dt.date.today(), parsed_time)

    # Add 30 minutes to the time
    new_time_datetime = time_datetime + dt.timedelta(minutes=30)
    return new_time_datetime

#Variables
servicios = ["Corte degradado - 20 $","Corte y Barba - 25 $","Barba - 10 $", "Tinte - 25 $"]
empleados = ["Diego","Gabriel"]
horas_disponibles = ['10:00', '10:30', '11:00', '11:30', '12:00', '12:30', '13:00', '13:30', '15:00', '15:30', '16:00', '16:30', '17:00', '17:30', '18:00', '18:30', '19:00']
credentials =  'test-calendar-420116-6df0ced01187.json' #st.secrets["db_credencial"]['credencial_calentar_json']  #'test-calendar-420116-6df0ced01187.json'
calendarid1 = st.secrets["db_credencial"]["smpt_username"] #correo del calendario en ID
calendarid2 = '3c286a0e2918ef7053872ef71e0b2892e3c64eaed80255963793e349957f304e@group.calendar.google.com'
timezone = 'America/Lima'
empleado = 'Diego'
document = 'app-citas'
sheet = 'citas'
#html_calendar = """<iframe src="https://calendar.google.com/calendar/embed?src=classtonidev%40gmail.com&ctz=Europe%2FMadrid" style="border: 0" width="800" height="600" frameborder="0" scrolling="no"></iframe>"""

#Page config
st.set_page_config(page_title="App de citas", page_icon="🪒", layout="centered")
st.image("assets/barberia.jpg")
st.title("Barberia de barrio")
st.text("Jiron intermedio Mz N4 Lt5, SJL")

selected = option_menu(menu_title=None, 
                       options=["Servicios","Reseñas","Portafolio","Detalles"],
                       icons= ["scissors","chat-dots","file-text","pin"], # https://icons.getbootstrap.com/
                       orientation="horizontal",
                       )

if selected == "Portafolio":
    st.image("assets/corte1.jpeg",caption="Degradado básico")
    st.image("assets/corte2.jpeg",caption="Corte más barba")
    st.image("assets/corte3.jpeg",caption="Raya personalizada")
    st.image("assets/corte4.jpg",caption="Afeitado personalizado")
    st.image("assets/corte5.jpg",caption="Corte tupe")

if selected == "Detalles":
    st.image("assets/map.JPG")
    st.markdown(f"Pulsa [aquí](https://www.google.com/maps/search/jiron+mariano+soto+mz+n4+lt5+urbanizacion+mariscal+caceres,+san+juan+de+lurigancho+,+lima+peru/@-11.9497517,-76.9803246,18z/data=!3m1!4b1?entry=ttu) para ver la dirección en Google Maps.")

    st.subheader("Empleados")
    column1, column2 = st.columns(2)
    column1.image("assets/barber1.png",caption="Julian")
    column2.image("assets/barber2.png",caption="Juan")

    st.subheader("Horarios de apertura y contacto")
    st.write("---")
    st.text("📞 920 187 327")
    st.write("---")

    c1,c2 = st.columns(2)
    c1.text("Lunes")
    c2.text("10:00 - 19:00")
    c1.text("Martes")
    c2.text("10:00 - 19:00")
    c1.text("Miercoles")
    c2.text("10:00 - 19:00")
    c1.text("Jueves")
    c2.text("10:00 - 19:00")
    c1.text("Viernes")
    c2.text("10:00 - 19:00")
    c1.text("Sabado")
    c2.text("10:00 - 19:00")
    c1.text("Domingo")
    c2.text("Cerrado")

    st.write("---")
    st.markdown("📷  [Instagram](www.instagram.com)")

if selected == "Reseñas":
    st.write("##")
    st.image("assets/opinion1.JPG")
    st.image("assets/opinion2.JPG")
    st.image("assets/opinion3.JPG")
    st.image("assets/opinion4.JPG")

if selected == "Servicios":

    #st.subheader("Calendario actual")
    #st.markdown(html_calendar,unsafe_allow_html=True)

    st.subheader("Reservar cita")
    a1,a2 = st.columns(2)
    nombre = a1.text_input("Tu nombre*")
    email = a2.text_input("Tu email*")
    fecha = a1.date_input("Fecha")
    if fecha:
        if empleado == 'Diego':
            calendarid = calendarid1
        elif empleado == 'Gabriel':
            calendarid =  'none' #calendarid2
        calendar = GoogleCalendar(credentials, calendarid) #Se crea el objetio de la clase GoogleCalendar
        hours_blocked = calendar.get_start_times(str(fecha)) #[]
        result_hours = np.setdiff1d(horas_disponibles,hours_blocked)
        #st.text(result_hours)

    st.text(hours_blocked)
    hora = a2.selectbox("Horas disponibles", result_hours)
    #st.text(hora)
    servicio = a1.selectbox("Servicio*", servicios)
    empleado = a2.selectbox("Empleado",empleados)
    nota = a1.text_area("💬 Nota (opcional)")

    enviar = st.button("Reservar")

    if enviar:
        if not nombre or not email or not servicio:
            st.warning("Tienes que rellenar todos los campos obligatorios antes de reservar tu cita")
        else:
            with st.spinner('Cargando ...'):
                #create event in google calendar
                precio = servicio.split("-")[1]      
                parsed_time = dt.datetime.strptime(hora, "%H:%M").time()
                #st.text(parsed_time)
                hours1 = parsed_time.hour
                st.text(hours1+1)
                minutes1 = parsed_time.minute
                end_hours = add_30_minutes(hora)
                start_time = dt.datetime(fecha.year, fecha.month, fecha.day, hours1-5, minutes1).astimezone(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S')
                #st.text(start_time)
                end_time = dt.datetime(fecha.year, fecha.month, fecha.day, end_hours.hour-5, end_hours.minute).astimezone(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S')
                summary = servicio+". "+ nombre
                if empleado == "Diego":
                    calendarid = calendarid1
                elif empleado == "Gabriel":
                    calendarid = calendarid2

                #crear evento en google calendar
                try:
                    calendar_manager = GoogleCalendar(credentials, calendarid)
                    calendar_manager.create_event(summary,start_time,end_time,timezone)
                except Exception as e:
                    st.warning("Ha habido un error al crear su cita, por favor intentelo más tarde.")

                #envio de correo
                send(email,nombre,fecha,hora,servicio,empleado)

                #guardar información en google sheet
                #try:
                    #data = [[nombre,email,str(fecha),str(hora),servicio,empleado,nota,precio]]
                    #google = GoogleSheet(credentials,document,sheet)
                    #range = google.get_last_row_range()
                    #google.write_data(range, data)
                #except Exception as e:
                    #print(e)

                #mensaje de exito
                st.success("Su cita ha sido creada correctamente")

    