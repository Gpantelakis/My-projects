# ----- CONFIGURE YOUR EDITOR TO USE 4 SPACES PER TAB ----- #
from datetime import datetime
import settings
import sys,os
sys.path.append(os.path.join(os.path.split(os.path.abspath(__file__))[0], 'lib'))
import pymysql as db
import random



def connection():
    ''' User this function to create your connections '''
    con = db.connect(
        settings.mysql_host, 
        settings.mysql_user, 
        settings.mysql_passwd, 
        settings.mysql_schema)
    
    return con

def mostcommonsymptoms(vax_name):
    
    # Create a new connection
    con=connection()
    # Create a cursor on the connection
    cur=con.cursor()

    #sql query
    sql="""select v.symptoms
            from vaccination v
            where  v.vaccines_vax_name='%s';
        """ % vax_name
    
    cur.execute(sql)

    result=cur.fetchall()
    list_results=list(result)
    new_result=list()
    for i in range(len(list_results)):
        str1=str(list_results[i])
        str2=str()
        str1=str1.lower()
        for letter in str1:
            if letter!=' ' and letter!=',' and letter!='(' and letter!=')' and letter!=';' and letter!='/' and letter!='.' and letter!='-' and letter!="'" and letter!='"' and letter!='\n':
                str2=str2+letter
            else:
                if str2!=str():
                    new_result.append(str2)
                    str2=str()
        if str2!=str():
            new_result.append(str2)
            str2=str()
         
    #print(result[0])

    #####################         STOPWORDS LIST    ##################################################
    stopwords=["i", "me", "my", "myself", "we", "our", "ours", "ourselves",                          #
    "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself",                 #
    "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their",                 #
    "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these",                 #
    "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has",                 #
    "had", "having", "do", "does", "did","didn", "doing", "a", "an", "the", "and", "but",            #
    "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with",                  #
    "about", "against", "between", "into", "through", "during", "before", "after",                   #
    "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over",                  #
    "under", "again", "further", "then", "once", "here", "there", "when", "where",                   #
    "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some",              #
    "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very",                  #
    "s", "t", "can", "will", "just", "don", "should", "now","later","continues"]                     #
    ##################################################################################################

    ### Remove Stopwords ###
    count=0
    for words in new_result:
        for word in stopwords:
            if words==word:
                new_result.pop(count) 
                break
        count=count+1

    
    print(new_result)
    
    return [("vax_name","result")]

    

def buildnewblock(blockfloor):
    
   # Create a new connection
    con=connection()
    
    # Create a cursor on the connection
    cur=con.cursor()

    #sql query
    sql=f"""select count(b.BlockCode)
            from block b
            where b.BlockFloor={blockfloor};
        """
    cur.execute(sql)

    result=cur.fetchone()
    N=0
    stop=False
    if result[0]<9:
        N=random.randint(0, 4)
        for i in [1,2,3,4,5,6,7,8,9]:
            sql=f"""INSERT INTO block(BlockFloor,BlockCode)
                VALUES({blockfloor},{i})
                """
            try:
                #execute the sql command
                cur.execute(sql)
                #Commit your changes in the database
                con.commit()
                Bcode=i
                stop=True
            except:
                print("Go next BlockCode")
                stop=False
            
            if stop==True:
                break

        for i in range(N+1):
            RoomNumber=str(blockfloor)+str(Bcode)+'0'+str(i)
            RoomNumber=int(RoomNumber)
            sql=f"""INSERT INTO room(RoomNumber,RoomType,BlockFloor,BlockCode,Unavailable)
                    VALUES({RoomNumber},'',{blockfloor},{Bcode},0)
                """
            try:
                #execute the sql command
                cur.execute(sql)
                #Commit your changes in the database
                con.commit()
            except:
                print("")
            
        return [("result"),"OK"]
    else:
        return [("result"),"ERROR"]

def findnurse(x,y):

    # Create a new connection
    con=connection()
    
    # Create a cursor on the connection
    cur=con.cursor()

    #sql query
    sql=f"""select distinct n.EmployeeID , n.Name ,count(distinct p.SSN)
            from nurse n, patient p,on_call oc,vaccination v1,vaccination v2
            where  oc.Nurse=n.EmployeeID  and  oc.BlockFloor={x} and n.EmployeeID=v1.nurse_EmployeeID and p.SSN=v2.patient_SSN and v1.patient_SSN=v2.patient_SSN 
            and v1.vaccination_date=v2.vaccination_date and v1.nurse_EmployeeID=v2.nurse_EmployeeID
            group by n.EmployeeID
            having count(distinct oc.BlockCode)>=all(select count(b.BlockCode) from  block b
									where b.BlockFloor={x}
									)
		    and count(distinct p.SSN)>{y}; 
        """

    #Execute command sql
    cur.execute(sql)

    #Fetch all the rows in a list of lists
    results=cur.fetchall()
    
    return [("Nurse", "ID", "Number of patients")] + list(results)
    
def patientreport(patientName):
    # Create a new connection
    con=connection()

    # Create a cursor on the connection
    cur=con.cursor()
    
    #sql query '1'
    sql=f"""select ph.Name
        from patient p,undergoes u,physician ph
        where p.SSN=u.Patient and u.Physician=ph.EmployeeID and p.Name='%s';
        """ % patientName
    #Execute command sql
    cur.execute(sql)

    #Fetch all the rows in a list of lists
    physician=cur.fetchone()
     

    #sql query '2'
    sql=f"""select n.Name
        from patient p,undergoes u,nurse n
        where p.SSN=u.Patient and n.EmployeeID=u.AssistingNurse and p.Name='%s';
        """% patientName
    #Execute command sql
    cur.execute(sql)

    #Fetch all the rows in a list of lists
    nurse=cur.fetchone()
    
    
    #sql query '3'
    sql=f"""select tr.Name
        from patient p,undergoes u,treatment tr
        where p.SSN=u.Patient and tr.Code=u.Treatment and p.Name='%s';
        """ % patientName
    #Execute command sql
    cur.execute(sql)

    #Fetch all the rows in a list of lists
    Tname=cur.fetchone()
    
    
    #sql query '4'
    sql=f"""select  tr.Cost
        from patient p,undergoes u,treatment tr
        where p.SSN=u.Patient and tr.Code=u.Treatment and p.Name='%s';
        """ % patientName
    #Execute command sql
    cur.execute(sql)

    #Fetch all the rows in a list of lists
    Tcost=cur.fetchone()
    
    
    #sql query '5'
    sql=f"""select s.StayEnd
        from patient p,undergoes u,stay s
        where p.SSN=u.Patient and s.StayID=u.Stay and p.Name='%s';
        """ % patientName
    #Execute command sql
    cur.execute(sql)

    #Fetch all the rows in a list of lists
    DateEnd=cur.fetchone()
    

    #sql query '5'
    sql=f"""select r.RoomNumber
        from patient p,undergoes u,stay s,room r
        where p.SSN=u.Patient and s.StayID=u.Stay and s.Room=r.RoomNumber and p.Name='%s';
        """ % patientName
    
    #Execute command sql
    cur.execute(sql)

     #Fetch all the rows in a list of lists
    RNumber=cur.fetchone()
    

    sql=f"""select r.BlockFloor
        from patient p,undergoes u,stay s,room r
        where p.SSN=u.Patient and s.StayID=u.Stay and s.Room=r.RoomNumber and p.Name='%s';
        """ % patientName
    #Execute command sql
    cur.execute(sql)

    #Fetch all the rows in a list of lists
    Floor=cur.fetchone()
    
    sql=f"""select r.BlockCode
        from patient p,undergoes u,stay s,room r
        where p.SSN=u.Patient and s.StayID=u.Stay and s.Room=r.RoomNumber and p.Name='%s';
        """ % patientName
    #Execute command sql
    cur.execute(sql) 

    #Fetch all the rows in a list of lists
    BlockC=cur.fetchone()
    
    return [("Patient","Physician", "Nurse", "Cost", "Treatement going on", "Date of Release", "Room", "Floor", "Block") , (patientName, physician, nurse ,Tcost ,Tname ,DateEnd, RNumber ,Floor,BlockC)]
