#1
select patient.SSN,patient.Name,count(undergoes.Stay)as Total_stay,sum(treatment.Cost)as Total_cost
from patient ,undergoes,treatment
where patient.SSN=undergoes.Patient and undergoes.Treatment=treatment.Code and patient.Age>=30 and patient.Age<=40 and patient.Gender='male'
group by undergoes.Patient
having count(distinct undergoes.Stay)>1;

#2
select nurse.EmployeeID,nurse.Name 
from nurse,room,on_call
where nurse.EmployeeID=on_call.Nurse and on_call.OnCallStart>='2008-04-20 23:22:00' and on_call.OnCallEnd<='2009-06-04 11:00:00'and on_call.BlockFloor>=4 and on_call.BlockFloor<=7
group by nurse.Name
having count(distinct on_call.BlockCode)>1;

#3
select patient.Name ,vaccination.patient_SSN,vaccines.num_of_doses
from vaccination,vaccines,patient
where patient.SSN=vaccination.patient_SSN and patient.Gender='female' and patient.Age>40
group by patient.SSN
having count(distinct vaccination.vaccination_date)=vaccines.num_of_doses;

#4
select medication.Name,medication.Brand,count(distinct prescribes.Patient)AS patients
from medication,prescribes
where prescribes.Medication=medication.Code
group by prescribes.Medication
having count(distinct prescribes.Patient)>1;

#5
select v1.patient_SSN
from vaccination v1
where not exists(select*
				 from vaccination v2
                 where v1.patient_SSN=v2.patient_SSN and v1.physician_EmployeeID!=v2.physician_EmployeeID
                );

#6
 SELECT 'yes' AS answer
 FROM room r,stay s
    WHERE exists(
    SELECT s.Room=r.RoomNumber AND s.StayStart>'2013-01-01 00:00:00' AND s.StayEnd>'2014-01-01 00:00:00')
 UNION
 SELECT 'no' AS answer
 FROM room r,stay s
    WHERE not exists(
    SELECT s.Room=r.RoomNumber AND s.StayStart>'2013-01-01 00:00:00' AND s.StayEnd>'2014-01-01 00:00:00');



#7
select distinct  p.Name,count(*)
from physician p ,undergoes u
where p.Position='PATHOLOGY' and u.Physician=p.EmployeeID 
group by p.EmployeeID
union
select distinct  p.Name,count(*)-1
from physician p 
where p.Position='PATHOLOGY' and not exists(select *
										from undergoes u
										where p.EmployeeID=u.Physician)
group by p.EmployeeID;

#8
select  p.Name
from patient p
where  not exists(select *
				 from vaccines v,vaccination vac
				 where vac.patient_SSN=p.SSN and vac.vaccines_vax_name=v.vax_name
				 group by p.Name
                 having count(vac.vaccination_date)=v.num_of_doses);
                 
# 9
select MAX(vax_name) 
from
    (select count(vac.vaccines_vax_name), vac.vaccines_vax_name as vax_name
    from vaccination vac
    group by vac.vaccines_vax_name) as allo;
    
#10
select distinct p.Name
from physician p,trained_in t,treatment t1
where p.EmployeeID=t.Physician and t.Speciality=t1.Code and t1.Name='RADIATION ONCOLOGY'