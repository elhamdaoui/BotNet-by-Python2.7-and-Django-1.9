var btn_id_click="nonn";
var color_click="#f0ad4e";
var corps=$("#corps");
var url_servr="http://127.0.0.1:8000/";
var data_cont_agent ="";

/* L'event de entrer la souris dans une bouton de navigation
*/
$("nav> div").mouseover( function() {
  if ( $(this).attr("id") != btn_id_click)
    $(this).css({"background-color":"#5cb85c"});
 });

 /* L'event de sortir la souris dans une bouton de navigation
 */
 $("nav> div").mouseout( function() {
   if ( $(this).attr("id") != btn_id_click)
      $(this).css({"background-color":"#0a0520"});//#BFBABB
  });

  /* L'event de click la souris dans une bouton de navigation
  */
  var remplir_apres_click=function(url,obj_rem){
    $.get(url,function(data){
      obj_rem.slideToggle("slow",function(){});
      obj_rem.html(data);
      obj_rem.slideDown("slow",function(){});
  	});
  };


  $("nav> div").click( function() {
  $("nav> div").css({"background-color":"#0a0520"});//#BFBABB
  $(this).css({"background-color":color_click});
  btn_id_click=$(this).attr("id");
  switch (btn_id_click) {
    case "cslt_agents":remplir_apres_click(url_servr+"serviceapp/clients/",corps);break;
    case "cslt_commandes":remplir_apres_click(url_servr+"serviceapp/getallcommandes/",corps);break;break;
    case "cslt_executions":alert("3");break;
    case "ajout_commandes":click_add_cmd();break;
    case "ajout_exec":alert("5");break;
    case "parametres":alert("6");break;
    case "developpers":alert("7");break;
    case "deconnexion":alert("8");break;
    default:;break;
  }
   });

/* l'event click sur le bouttn info d'agent
*/
var info_agent_click=function(id_a){
  $.post(url_servr+"serviceapp/getclient/",{id_client: id_a},function(data){
    $("#myLargeModalLabel").text("Informations sur un agent");
    $("#myLargeModalLabel").css({"color":"#5cb85c"});
    $("#myLargeModalContenu").html(data);
    $("#myLargeModalFooter").html('<button type="button" class="btn btn-warning" title="S\'Affecter des commandes"><span class="glyphicon glyphicon-plus-sign" aria-hidden="true"></span></button>\
    <button type="button" class="btn btn-info" title="Voir ses commandes"  onclick="click_cmds_agent();" id="vu_cmds_ag"><span class="glyphicon glyphicon-paperclip" aria-hidden="true"></span></button>\
    <button type="button" class="btn btn-success" title="Modifier" data-toggle="modal" data-target="#myModal" onclick="click_mod_agent();"><span class="glyphicon glyphicon-pencil" aria-hidden="true"></span></button>\
    <button type="button" class="btn btn-danger" title="Supprimer" data-toggle="modal" data-target="#myModal" onclick="click_supp_agent();"><span class="glyphicon glyphicon-remove-circle" aria-hidden="true"></span></button>\
    <input type="hidden" class="btn btn-default" data-dismiss="modal" id="anul_large_model"/>'
  );
  });
  $("#myLargeModalFooter").slideDown("slow",function(){});
};

/*remplir les nav de infos persos et infos techniques*/
var click_infos_tech_pers=function(num){
    $("#contenu_infoos").slideToggle("fast",function(){});
    if(num!=1){
    $("#contenu_infos_tech").css({"display":"block"});
    $("#contenu_infos_pers").css({"display":"none"});
  }else{
    $("#contenu_infos_tech").css({"display":"none"});
    $("#contenu_infos_pers").css({"display":"block"});
  }
    $("#contenu_infoos").slideDown("slow",function(){});
};

/*supprimer un agent */
var supp_agent=function(id_bot){
    $.post(url_servr+"serviceapp/delclient/",{id_client: id_bot},function(data){
      var start_not="supprimé avec succès";
      var ind_not=data.indexOf(start_not);
      $("#myModalLabel").text("Suppression");
      $("#myModalContenu").html(data);
      $("#myModalFooter").html('<button type="button" class="btn btn-default" data-dismiss="modal">Ok</button>');
      if(ind_not>-1){
        $("#anul_large_model").trigger("click",function(){});
        $("#cslt_agents").trigger("click",function(){});
        }
});
};
var click_supp_agent=function(){
  $("#myModalLabel").text("Voulez-vous vraiment supprimer cet agent et ses executions?");
  $("#myModalLabel").css({"color":"#c12e2a"});
  $("#myModalContenu").html("Utilisateur: <font style='font-weight:bold;color:#5cb85c;'>"+$("#user_bot").text()+"</font>, Hôte:<font style='font-weight:bold;color:#5cb85c;'>"+$("#host_bot").text()+"</font>");
  var id_bot=$("#id_bot").text();
  $("#myModalFooter").html('<button type="button" class="btn btn-default" data-dismiss="modal">Annuler</button>\
  <button type="button" class="btn btn-danger" onclick="supp_agent('+id_bot+');">Supprimer</button>');
};

/*Modifier un agent */
var mod_agent=function(){
    var id_bot=$("#id_bot").text();
    var act_bot=document.getElementById("val_actif").checked;
    $.post(url_servr+"serviceapp/modclient/",{id_client: id_bot, actif:act_bot},function(data){
      $("#myModalLabel").text("Modification");
      $("#myModalContenu").html(data);
      $("#myModalFooter").html('<button type="button" class="btn btn-default" data-dismiss="modal">Ok</button>');

});


};
var click_mod_agent=function(){
  var ac_bot=$("#act_bot").text();
  var ckeched_v=(ac_bot=="True")? "checked='true'":"";
  $("#myModalLabel").text("Modifier un agent");
  $("#myModalLabel").css({"color":"#c12e2a"});
  $("#myModalContenu").html('Utilisateur: <font style="font-weight:bold;color:#5cb85c;">'+$('#user_bot').text()+'</font>, Hôte:<font style="font-weight:bold;color:#5cb85c;">'+$('#host_bot').text()+'</font><br/><br/>\
  <div class="row">\
  <div class="col-lg-12">\
    <div class="input-group">\
      <span class="input-group-addon">\
        <input type="checkbox" aria-label="..." id="val_actif" '+ckeched_v+'>\
      </span>\
      <label class="form-control" aria-label="...">Actif, la désactivation de cet option s\'arrête la communication</label>\
    </div>\
  </div>');
  $("#myModalFooter").html('<button type="button" class="btn btn-default" data-dismiss="modal">Annuler</button>\
  <button type="button" class="btn btn-success" onclick="mod_agent();">Modifier</button>');
};

/*Afficher les commandes d'un agent*/
var click_cmds_agent=function(){
  var id_bot=$("#id_bot").text();
  $("#myLargeModalLabel").html("les commandes de l'agent, Utilisateur: <font style='font-weight:bold;color:#c12e2a;'>"+$("#user_bot").text()+"</font>, Hôte: <font style='font-weight:bold;color:#c12e2a;'>"+$("#host_bot").text()+"</font>");
  //alert("ID"+id_bot);
  $.post(url_servr+"serviceapp/getcmdsclient/",{id_client: id_bot},function(data){
      data_cont_agent=$("#myLargeModalContenu").html();
      $("#myLargeModalFooter").slideToggle("slow",function(){});
      $("#myLargeModalContenu").html(data);

    //  alert("ba1");
        //alert(typeof document.getElementById("#vu_cmds_ag").id);
    });
  //$("#myModalLabel").css({"color":""});
  /*$("#myModalContenu").html("Utilisateur: <font style='font-weight:bold;color:#5cb85c;'>"+$("#user_bot").text()+"</font>, Hôte:<font style='font-weight:bold;color:#5cb85c;'>"+$("#host_bot").text()+"</font>");
  var id_bot=$("#id_bot").text();
  $("#myModalFooter").html('<button type="button" class="btn btn-default" data-dismiss="modal">Annuler</button>\
  <button type="button" class="btn btn-danger" onclick="supp_agent('+id_bot+');">Supprimer</button>');
  */
};

var back_info_agent=function(){
  $("#myLargeModalContenu").html(data_cont_agent);
  $("#myLargeModalFooter").slideDown("slow",function(){});
};

/*==============================================*/
/*Créer une classe pour gérer les commandes (supp, mod, del, afectation)*/
var url_gr_cmd=url_servr+"serviceapp/gerercommande/";

var commande_afficher=function(id_c){
  $("#myLargeModalLabel").html('<div style="font-weight:bold;" class="text-success">Commande infos</div>');
  $.post(url_gr_cmd,{id_cmd: id_c,"action":"afficher"},function(data){
      //data_cont_agent=$("#myLargeModalContenu").html();
      $("#myLargeModalFooter").hide("fast");
      $("#myLargeModalContenu").html(data);
    });
};
var commande_supprimer=function(id_c){
  $("#myModalLabel").html('<div class="text-danger">Voulez-vous supprimer cette commandes et ses executions ?</div>');
  $("#myModalContenu").html('');
  $("#myModalFooter").html('<button type="button" class="btn btn-default" data-dismiss="modal">Annuler</button>\
  <button type="button" class="btn btn-danger" onclick="commande_supp_bdd('+id_c+')">Supprimer</button>');
};
var commande_supp_bdd=function(id_c){
  $.post(url_gr_cmd,{id_cmd: id_c,"action":"supprimer_bdd"},function(data){
      //data_cont_agent=$("#myLargeModalContenu").html();
      $("#myModalContenu").html(data);
    });
  $("#myModalFooter").html('<button type="button" class="btn btn-default" data-dismiss="modal">Ok</button>');
};

var commande_modifier=function(id_c){
  $("#myLargeModalLabel").html('<div class="text-success">Modifier une Commande</div>');
  $.post(url_gr_cmd,{id_cmd: id_c,"action":"modifier"},function(data){
      //data_cont_agent=$("#myLargeModalContenu").html();
      $("#myLargeModalContenu").html(data);//formulaire
      $("#myLargeModalFooter").html('<button type="button" class="btn btn-default" data-dismiss="modal">Annuler</button>');
  });
};
var commande_affecter_agent=function(id_c){
  $("#myLargeModalLabel").html('<div class="text-success">Ajouter des executeurs au cette commande</div>');
  $.post(url_gr_cmd,{id_cmd: id_c,"action":"affecter"},function(data){
      //data_cont_agent=$("#myLargeModalContenu").html();
      $("#myLargeModalContenu").html(data);//formulaire
      $("#myLargeModalFooter").html('<button type="button" class="btn btn-default" data-dismiss="modal">Annuler</button>');
    });
};

/*=================================================*/
/*modifier une commande d'un client */
var exe_in=-1;
var click_mod_client_commande=function(id_cl,id_cm){
  $.post(url_servr+"serviceapp/modcmdclient/",{id_cmd: id_cm, id_client:id_cl, action:"exec_cslt"},function(data){
    ckeched_v= (data=='True')?'checked="true"':'';
    $("#myModalLabel").html("<div class='alert-warning'>Modifier une commande d'un agent !!</div>");
    $("#myModalContenu").html('<div class="row">\
    <div class="col-lg-12">\
      <div class="input-group">\
        <span class="input-group-addon">\
          <input type="checkbox" aria-label="..." id="val_exec_1c" '+ckeched_v+'>\
        </span>\
        <label class="form-control text-danger" aria-label="...">Exécutée, désactive l\'execution de cette commmande par cet agent.</label>\
      </div>\
    </div>');
    $("#myModalFooter").html('<button type="button" class="btn btn-default" data-dismiss="modal">Annuler</button>\
    <button type="button" class="btn btn-success" onclick="mod_client_commande_hh('+id_cl+','+id_cm+');">Ok</button>');
    $("#myModalFooter").show();
  });

};
var mod_client_commande_hh=function(id_cl,id_cm){
  var exe=document.getElementById("val_exec_1c").checked;
  $.post(url_servr+"serviceapp/modcmdclient/",{id_cmd: id_cm, id_client:id_cl, action:"modif", executee:exe},function(data){
    $("#myModalContenu").html(data);
    $("#myModalFooter").hide();
    $.post(url_servr+"serviceapp/getcmdsclient/",{id_client: id_cl},function(data){
        $("#myLargeModalContenu").html(data);
      });
  });
};


/*=================================*/
var click_btn_execs_cmd_cli=function(id_cli, id_cm){
  $.post(url_servr+"serviceapp/execscmdclient/",{id_cmd: id_cm, id_client:id_cli},function(data){
      //alert(data);
    $("#corps").html(data);

  });
};

/*=================================*/
var supp_execut_ion=function(id_e,type_ex,id_div){
  if(confirm("Voulez-vous vraiment de supprimer cette execution ?")){
    $.post(url_servr+"serviceapp/modexecution/",{id_ae:id_e, type_ae:type_ex, action:"supprimer"},function(data){
        if(data=="0"){
          alert("Erreur: cette execution n'est pas supprimer");
        }else{
          $("#"+id_div).hide("slow");
        }
    });
  }
};

/*=========Ajouter commande=======*/
var click_add_cmd=function(){
  var fixedtex='<div class="navbar navbar-inverse">\
  <div class="btn-group">\
  <button type="button" class="btn btn-default btn-lg dropdown-toggle" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">\
    Type de commande<span class="caret"></span>\
  </button>\
  <ul class="dropdown-menu">\
    <li><a href="#" onclick="affich_forms(\'KeyLogger\');">KeyLogger</a></li>\
    <li><a href="#" onclick="affich_forms(\'ScreenShot\');">ScreenShot</a></li>\
    <li role="separator" class="divider"></li>\
    <li><a href="#" onclick="affich_forms(\'Download\');">Download</a></li>\
    <li><a href="#" onclick="affich_forms(\'Upload\');">Upload</a></li>\
    <li><a href="#" onclick="affich_forms(\'Shell\');">Shell</a></li>\
  </ul>\
</div>\
  </div>\
  <div id="cont_for_add">\
  </div>';

  $("#corps").hide("fast");
  $("#corps").html(fixedtex);
  $("#corps").show("slow");

  $.post(url_servr+"serviceapp/addcmdforms/",{type_cmd:"KeyLogger",action:"forms"},function(data){
    $("#cont_for_add").hide("fast");
    $("#cont_for_add").html(data);
    $("#cont_for_add").show("slow");
  });
};

var affich_forms=function(type_c){
  $.post(url_servr+"serviceapp/addcmdforms/",{type_cmd:type_c,action:"forms"},function(data){
    $("#cont_for_add").hide("fast");
    $("#cont_for_add").html(data);
    $("#cont_for_add").show("slow");
  });
};

var ajouter_commande=function(){
  //alert("jaoutr");
  type_cm=document.getElementById("type_add").value;
  titre_cm=document.getElementById("titre_add").value;
  cm_db=document.getElementById("date_debut_add").value;
  cm_df=document.getElementById("date_fin_add").value;
  cm_tx=document.getElementById("texte_add").value;
  cm_url="";
  if(document.getElementById("url_add")!=null)
    cm_url=document.getElementById("url_add").value;
    //alert("lllll");
    $.post(url_servr+"serviceapp/addcmdforms/",{type_cmd:type_cm,titre_cmd:titre_cm,cmd_db:cm_db, cmd_df:cm_df,cmd_tx:cm_tx, cmd_url:cm_url,action:"add"},function(data){
      $("#cont_for_add").hide("fast");
      $("#cont_for_add").html(data);
      $("#cont_for_add").show("slow");
    });
    alert("Requet d'ajout terminée");
    //return false;
};
