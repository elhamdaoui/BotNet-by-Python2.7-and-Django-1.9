var url_serveur="http://127.0.0.1:8000/";
var url_notif="http://127.0.0.1:8000/serviceapp/notifications/";
var data_not_ag="",data_not_exec="",data_not_cmds="";

var html_btn_close='<button style="position:fixed;background-color:red;top:5.2%;" type="button" class="close" aria-label="Close" onclick="$(\'#cont_notofications\').hide(\'slow\');"><span aria-hidden="true">&times;</span></button>';
/*Gerer les nouveaux agents*/
var notif_new_agents=function(){
  var tex=$("#val_new_agents").text();
  $.post(url_notif,{notif:'newagents'},function(data){
      var tab=data.split("\n");
      //alert(tab.join("\n---\n"));
      nb=tab[1].split("-")[1];
      if(nb>0){
        $("#val_new_agents").css({"opacity":"1"});
      }else{
        $("#val_new_agents").css({"opacity":"0"});
      }
      $("#val_new_agents").text(nb);
      data_not_ag=tab.slice(2).join("");
  });
};

/*Nptifications commandes*/
var notif_new_cmds=function(){
  $.post(url_notif,{notif:'newcommandes'},function(data){
      var tab=data.split("\n");
      nb=tab[1].split("-")[1];
      if(nb>0){
        $("#val_new_cmd_execs").css({"opacity":"1"});
      }else{
        $("#val_new_cmd_execs").css({"opacity":"0"});
      }
      $("#val_new_cmd_execs").text(nb);
      data_not_cmds=tab.slice(2).join("");
  });
};

/*Nptifications Executions*/
var notif_new_executions=function(){
  $.post(url_notif,{notif:'newexecutions'},function(data){
      var tab=data.split("\n");
      nb=tab[1].split("-")[1];
      if(nb>0){
        $("#val_new_executions").css({"opacity":"1"});
      }else{
        $("#val_new_executions").css({"opacity":"0"});
      }
      $("#val_new_executions").text(nb);
      data_not_exec=tab.slice(2).join("");
  });
};

/*Notifications*/
var Notifications=function(){
  notif_new_agents();
  notif_new_cmds();
  notif_new_executions();
};

/*lancer plugin*/
Notifications();
setInterval(Notifications, 5000);

/*events click btns notifications*/
$("#new_agents").bind("click",function(){
  $("#cont_notofications").slideToggle("fast",function(){});
  $("#cont_notofications").html(html_btn_close+" "+data_not_ag);
  $("#cont_notofications").slideDown("slow",function(){});
});

$("#new_cmd_execs").bind("click",function(){
  $("#cont_notofications").slideToggle("fast",function(){});
  $("#cont_notofications").html(html_btn_close+" "+data_not_cmds);
  $("#cont_notofications").slideDown("slow",function(){});
});

$("#new_executions").bind("click",function(){
  $("#cont_notofications").slideToggle("fast",function(){});
  $("#cont_notofications").html(html_btn_close+" "+data_not_exec);
  $("#cont_notofications").slideDown("slow",function(){});
});

/*Appel des fcts bootstrap pour activer des fonctionnalités des notifications*/
$(function () {
  $('[data-toggle="tooltip"]').tooltip();
});

/*click sur le bouton vue de notification agent*/
var agentvue=function(elt,id_c){
  var vue_e= elt.hasClass('btn-default')? true:false;
  //alert(vue_e);
  $.post(url_serveur+"serviceapp/modclient/",{id_client:id_c,vue:vue_e},function(data){
    if(vue_e){
      elt.toggleClass('btn-default');
      elt.addClass('btn-success');
    }else{
      elt.toggleClass('btn-success');
      elt.addClass('btn-default');
    }
  });
};


/*click sur le bouton vue de notification commande exécutée*/
var newcmdvue=function(elt,id_cl,id_cm){
  var vue_e= elt.hasClass('btn-default')? true:false;
  //alert(vue_e);
  $.post(url_serveur+"serviceapp/modcmdclient/",{id_client:id_cl, id_cmd:id_cm, vue_exec:vue_e},function(data){
    if(vue_e){
      elt.toggleClass('btn-default');
      elt.addClass('btn-success');
    }else{
      elt.toggleClass('btn-success');
      elt.addClass('btn-default');
    }
  });
};

/*click sur le bouton vue de notification execution */
var newexecvue=function(elt,id_e,type_e){
  var vue_e= elt.hasClass('btn-default')? true:false;
  $.post(url_serveur+"serviceapp/modexecution/",{id_ae:id_e, type_ae:type_e, vue_exec:vue_e},function(data){
    if(vue_e){
      elt.toggleClass('btn-default');
      elt.addClass('btn-success');
    }else{
      elt.toggleClass('btn-success');
      elt.addClass('btn-default');
    }
  });
};
