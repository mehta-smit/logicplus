from .lpdb import dbcon
from .course import course
from .batch import batch


class admission():
    def updatecourse(self, aid):
        cname, fees = course().getcname(aid)
        update = "update lp.admission_trnxs set course='%s',fees=%d where id=%d;" % (str(cname), fees, aid)
        print(len(cname))
        return dbcon().do_insert(update)

        """
        select = "select course,fees from lp.admission_trnxs WHERE id=%d;" % (int(data['aid']))
        print(select)
        ad_data = dbcon().do_select(select)
        if data['cname'] not in ad_data[0][0]:
            data['cname'] = ad_data[0][0] + ',' + str(data['cname'])
            fees = int(data['fees']) + ad_data[0][1]
            update = "update lp.admission_trnxs set course='%s',fees=%d WHERE id=%d;" % (data['cname'], fees, int(data['aid']))
            print(update)
            return dbcon().do_insert(update)
        """

    def addAdmission(self,name,phone,email,study,cname,address,gender,join,fees,details,bid):
        insert = "insert into lp.admission_trnxs(name,phone,email,study,course,address,gender,join_date,fees,active,dp,details,bid) values('%s','%s','%s','%s','%s','%s','%s','%s','%s','1','%s','%s',%d);"%(name,phone,email,study,cname,address,gender,join,fees,'profile-pic.jpg',details,int(bid))
        if dbcon().do_insert(insert):
            aid = self.getIdByPhone(phone)
            return aid[0][0]

    def updateAddmission(self,name,phone,email,study,cname,address,gender,join,fees,details,bid,id):
        update = "update lp.admission_trnxs set name='%s',phone='%s',email='%s',study='%s',course='%s',address='%s',gender='%s',join_date='%s',fees=%d,details='%s',bid=%d where id=%d;"%(name,phone,email,study,cname,address,gender,join,int(fees),details,int(bid),int(id))
        return dbcon().do_insert(update)

    def getIdByPhone(self,phone):
        select = "select id from lp.admission_trnxs where phone='%s';"%(phone)
        return dbcon().do_select(select)

    def updatedpById(self,dp,id):
        update = "update lp.admission_trnxs set dp='%s' where id=%d;"%(dp,id)
        return dbcon().do_insert(update)

    def getAdmission(self, id=0):
        if id == 0:
            select = "select * from lp.admission_trnxs order by id;"
        else:
            select = "select * from lp.admission_trnxs where id=%d;"%id
        return dbcon().do_select(select)

    def active(self, id):
        update = "update lp.admission_trnxs set active='1' where id=%d;"%id
        return dbcon().do_insert(update)

    def delete(self, id):
        update = "update lp.admission_trnxs set active='0' where id=%d;"%id
        return dbcon().do_insert(update)

    def getstudentNameByCid(self, cid):
        course_name = course().getCourseName(cid)
        select = "select id,name from lp.admission_trnxs where course='%s';"%course_name[0]
        return dbcon().do_select(select)

    def getstudentImageById(self, id):
        select = "select dp,fees from lp.admission_trnxs where id=%d;" % int(id)
        return dbcon().do_select(select)

    def getInvoiceGeneratedata(self,id):
        select = "select id,name,phone,email,course,address,fees from lp.admission_trnxs where id=%d;"%int(id)
        return dbcon().do_select(select)

    def getstudentfees(self, aid):
        select = "select fees from lp.admission_trnxs where id=%d;"%aid
        return dbcon().do_select(select)

    def getInvoiceData(self,course_name=None,faculty_name=None):
        if course_name != 'ALL' and course_name is not None:
            course_name = course_name.split(':')
            course_id = course_name[0]
            course_name = course_name[1]

        if (course_name is None and faculty_name is None) or (course_name == 'ALL' and faculty_name == 'ALL'):
            select = "select lp.admission_trnxs.id,name,course,lp.admission_trnxs.fees,(lp.admission_trnxs.fees-sum(lp.invoice_trnxs.fees)) as remaining_fees,phone,count(lp.invoice_trnxs.aid) as installment_no,lp.admission_trnxs.bid from lp.admission_trnxs inner join lp.invoice_trnxs on lp.invoice_trnxs.aid=lp.admission_trnxs.id group by lp.admission_trnxs.id;"
            result1 = dbcon().do_select(select)

            for r in range(0,len(result1)):
                select = "select lp.faculty.name from lp.faculty,(select lp.batch_trnxs.fid from lp.batch_trnxs,lp.admission_trnxs where lp.batch_trnxs.bid=%d) as fid where lp.faculty.id=1;"%int(result1[r][7])
                result2 = dbcon().do_select(select)
                result1[r] += result2[r]
            return result1
        elif course_name == 'ALL':
            select = "select lp.admission_trnxs.id,name,course,lp.admission_trnxs.fees,(lp.admission_trnxs.fees-sum(lp.invoice_trnxs.fees)) as remaining_fees,phone,count(lp.invoice_trnxs.aid) as installment_no,lp.admission_trnxs.bid from lp.admission_trnxs inner join lp.invoice_trnxs on lp.invoice_trnxs.aid=lp.admission_trnxs.id group by lp.admission_trnxs.id;"
            result1 = dbcon().do_select(select)

            for r in range(0, len(result1)):
                select = "select lp.faculty.name from lp.faculty,(select lp.batch_trnxs.fid from lp.batch_trnxs,lp.admission_trnxs where lp.batch_trnxs.bid=%d) as fid where lp.faculty.id=1;" % int(result1[r][7])
                result2 = dbcon().do_select(select)
                result1[r] += result2[r]
            return result1
        elif faculty_name == 'ALL':
            select = "select lp.admission_trnxs.id,name,course,lp.admission_trnxs.fees,sum(lp.invoice_trnxs.fees),phone,count(lp.invoice_trnxs.aid) as installment_no,lp.admission_trnxs.bid from lp.admission_trnxs inner join lp.invoice_trnxs on lp.invoice_trnxs.aid=lp.admission_trnxs.id where course='%s' group by lp.admission_trnxs.id;"%course_name
            result1 = dbcon().do_select(select)

            for r in range(0, len(result1)):
                select = "select lp.faculty.name from lp.faculty,(select lp.batch_trnxs.fid from lp.batch_trnxs,lp.admission_trnxs where lp.batch_trnxs.bid=%d) as fid where lp.faculty.id=1;" % int(result1[r][7])
                result2 = dbcon().do_select(select)
                result1[r] += result2[r]
            return result1
        else:
            select = "select lp.admission_trnxs.id,name,course,lp.admission_trnxs.fees,(lp.admission_trnxs.fees-sum(lp.invoice_trnxs.fees)) as remaining_fees,phone,count(lp.invoice_trnxs.aid) as installment_no,lp.admission_trnxs.bid from lp.admission_trnxs inner join lp.invoice_trnxs on lp.invoice_trnxs.aid=lp.admission_trnxs.id where course='%s'group by lp.admission_trnxs.id;" % course_name
            result1 = dbcon().do_select(select)

            for r in range(0, len(result1)):
                select = "select lp.faculty.name from lp.faculty,(select lp.batch_trnxs.fid from lp.batch_trnxs,lp.admission_trnxs where lp.batch_trnxs.bid=%d) as fid where lp.faculty.id=1;" % int(result1[r][7])
                result2 = dbcon().do_select(select)
                result1[r] += result2[r]
            return result1

    def coountid(self):
        select = "select count(id) from lp.admission_trnxs;"
        count = dbcon().do_select(select)
        return count[0][0]


class admission_batch():
    def add(self, aid, bid, time):
        select = "select aid,bid from lp.admission_batch where aid=%d AND bid=%d;" % (aid, bid)
        result = dbcon().do_select(select)
        print('len', len(result))
        if len(result) == 0:
            insert = "insert into lp.admission_batch(aid, bid, time) VALUES(%d,%d,'%s');" % (aid, bid, time)
            del aid, bid, select, result
            return dbcon().do_insert(insert)
        else:
            del aid, bid, select, result
            return True

    def getdt(self, aid, bdata):
        select = "select bid,time from lp.admission_batch where aid=%d;" % aid
        bid = dbcon().do_select(select)

        for i in range(len(bid)):
            bid[i] = bid[i] + batch().getdtbybid(bid[i][0])

        print(bid)

        time_clash = False
        # extract bid from batch data
        bdata = bdata.split('_')
        bid_org = bdata[0]

        # extract day and time from batch data
        dati = bdata[1].split(' ')
        time = dati[1]
        day = dati[0].split(',')
        print("bdata==", bdata)
        for i in range(len(bid)):
            if int(bid_org) != bid[i][0]:
                # check day and time clash
                for d in day:
                    if d in bid[i][2]:
                        if time in bid[i][1]:
                            time_clash = True
                            print("time match==", time_clash)
                            return True
                        else:
                            time_clash = False
            else:
                # if no time clashing
                time_clash = True
                print("id match==", time_clash)
                return True
        return time_clash

    def getbid(self, aid):
        select = "select bid from lp.admission_batch where aid=%d order by bid;" % aid
        bid = dbcon().do_select(select)

        for i in range(len(bid)):
            for j in range(len(bid[i])):
                bid[i] = bid[i][j]
        return bid


if __name__ == "__main__":
    admission_batch(), admission()