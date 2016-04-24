$(function(){
    showSelectBox();
    selectOnRed();
    controlCount();
    siteed();
    siteSearch();
    showCookMark();
    btnUnbind();
    agreed();
    showCook();
    tipsDelay();
    /*controlPosition();*/
    showMark();
    closeMarkBox();
    agreeRadio();
    agreeRadio2();
    aBtnMoreShow();
    bodyClick();    
});

var selectConhideflag=true;
function bodyClick(){
    $("body").click(function(){    
        if(selectConhideflag){    
        var aTxt =$("a[data-select]");
        aTxt.each(function(){
            var selectCon=$(this).siblings("ul");
                   selectCon.hide(); 
        });
        }else{
            selectConhideflag=true;
        }
    });

}
function showSelectBox(){
    var aTxt =$("a[data-select]");
    aTxt.each(function(){
        var selectCon=$(this).siblings("ul");
        var selectConNext=$(this).parent("div").siblings("div").children("ul");
                       $(this).click(function(){
                           selectConhideflag=false;
                           var span=$(this).children('span');
                           span.css("color","#fff");
                           selectCon.toggle();
                           selectConNext.hide();
                           selectCon.children("li").each(function(){
                               $(this).click(function(){
                               if(!$(this).hasClass("prev")){
                                   span.html($(this).html());
                                   selectCon.hide();
                                   //alert($(this).attr("menudate"));

                                   //save shopping basket 2016/04/12
                                    param="";
                                    $(".cook_info").each(function(){
                                      cnt = $(this).find('.count').html();
                                      id = $(this).children("input").val();
                                      if(cnt > 0){
                                          param = id+"_"+cnt+"|"+param;
                                      }
                                    });

                                   if (typeof($(this).attr("menudate")) != "undefined"){
                                       menudate = $(this).attr("menudate");
                                       if(param!=""){
                                           location.href = "/menus?menudate="+menudate+"&param="+param;
                                        }
                                        else{
                                           location.href = "/menus?menudate="+menudate;
                                        }
                                   }
                               }    
                               });
                           });  
                                               
                       });
    });
}


var locations = [];
var addLocation = function(l){
    locations.push(l);
};
//定位
function siteed(){    
    $("div[data-conlists]").find("li").each(function(){
                       $(this).click(function(){
                               var l = {};
                               l.level = $(this).parent("ul").data("level");
                               l.name = $(this).html();
                               addLocation(l);

                               //获取所选择的位置的值
                               var pSpan=$("div[data-conlists]").siblings("p[data-select]").children("span");
                               var pSpanHtml="";
                               if( $(this).parent("ul").data("level")=="1"){
                                   pSpanHtml=$(this).html();
                               }else{
                    pSpanHtml=pSpan.html() + "-"+ $(this).html();
                               }
                               pSpan.html(pSpanHtml);

                               $("div[data-conlists]").siblings("p[data-select]").children("a[data-btnreturn]").show();
                               
                               var thisData =$(this).data("p");
                               var allUl=$("div[data-conlists]").children("ul");
                               for(var i=0;i<allUl.length;i++){
                                   if($(allUl[i]).data("p")==thisData){
                                       //console.info($(allUl[i]).data("p",thisData));
                                       $(allUl[i]).data("p",thisData).show();
                                   }else{
                                       $(allUl[i]).hide();
                                   }
                               }
            if($(this).data("link")){
                        $("[data-conlists]").children("ul").hide();
                        location.href = $(this).data("link");   
                       }
                   aBtnMoreShow();
                       });
    });
}

 $("[data-btnreturn]").click(function(){
     var lastLocation = locations.pop();

     if(lastLocation != undefined){
         var level = lastLocation.level;
         var names = "";
         for(var i=0;i < locations.length;i++){
             if(i==locations.length-1){
                names += locations[i].name;
             }else{
                names += locations[i].name + "-";
             }
             
         }
 
         var pSpan=$("div[data-conlists]").siblings("p[data-select]").children("span");
        if(level == 1){
            pSpan.html("请选择送餐区域");
            $(this).hide();
        }else{
            pSpan.html(names);
        }
                           
       var allUl=$("div[data-conlists]").children("ul");
       for(var i=0;i<allUl.length;i++){
           if($(allUl[i]).data("level")==level){
               $(allUl[i]).show();
           }else{
               $(allUl[i]).hide();
           }
       }
    aBtnMoreShow();
    }
 });

//收藏
function selectOnRed(){
    var aStore =$("a[data-store]");
    aStore.click(function(){
        if($(this).hasClass("on")){
            $(this).removeClass("on");
        }else{
            $(this).addClass("on");
        }
    });    
}
//加减数目
function add (numSpan,o,stock){
        numSpan.html(parseInt(numSpan.html())+1);
            o.siblings("a[data-minus]").addClass("on");
            o.siblings().show();
            if(parseInt(numSpan.html())==parseInt(stock)){
                o.addClass("no");
                o.unbind("click");
            }    
}
function controlCount(){
    
    $("a[data-add]").each(function(){
        $(this).click(function(){    
            var numSpan   = $(this).siblings("span[data-count]");
            var stock = $(this).attr("stock");
            //alert(stock);
            add(numSpan,$(this),stock);

            $(".news_num").html(parseInt($(".news_num").html())+1);
        });    
    });

    $("a[data-minus]").each(function(){
        $(this).click(function(){
            var numSpan = $(this).siblings("span[data-count]");    
            numSpan.html(parseInt(numSpan.html())-1);

            $(".news_num").html(parseInt($(".news_num").html())-1);

            if(numSpan.html()==0){
                numSpan.html("0");
                $(this).hide();
                $(this).next("span").hide();
            }else if(parseInt(numSpan.html())==max-1){
                $(this).siblings("a[data-add]").removeClass("no");
                $(this).siblings("a[data-add]").bind("click",function(){
                    add(numSpan,$(this));
                });
            }

        });
    });

}

function siteSearch(){
    $("a[data-sitesearch]").click(function(){
        $(this).hide();
        $(this).siblings("p[data-select]").hide();
        $(this).siblings("div[data-inputbox]").show();
        $(this).siblings(".con_lists").children("ul[data-location]").hide();
    });
}
//判断菜单是否展开，展开返回true
var menuing = function(){
    var flag = false;
    var aTxt =$("a[data-select]");
    aTxt.each(function(){
        var selectCon=$(this).siblings("ul");
        if(selectCon.is(":visible")){
            flag = true;
        }
    });
    return flag;    
};

//点击显示图片详情
function showCookMark(){
    $("[data-cookimg]").each(function(){
        $(this).click(function(){
            
            if(!menuing()){//菜单不展开才执行！
                $(this).siblings("[data-markInfo]").show();
                $(this).siblings("[data-markInfo]").click(function(){
                    
                    if(!menuing()){//菜单不展开才执行！
                        $(this).hide();
                    }
                    
                });            
            }
            
        });
    });
}
//展开菜单详情
function showCook(){
    $("[data-detail]").each(function(){
        $(this).click(function(){
            $(this).children(".icon").toggle();
            $(this).children(".detail").toggle();
            $(this).children(".detailbox").toggle();
        });
    });
}
function btnUnbind(){
    $("[data-getgray]").each(function(){
        $(this).click(function(){
            $(this).addClass('no');
            $(this).children("span").show();
            //$(this).unbind("click");
        });
    });
}
function agreed(){
    $(".agree_txt").click(function(){
        if($(this).children("a").hasClass("on")){
            $(this).children("a").removeClass("on");
            $(this).parent("li").parent("ul").siblings(".btn_red_wrap").addClass('no');
            hideAgreeMore();
            alert($this.html());
        }else{
            $(this).children("a").addClass("on");
            showAgreeMore();
            $(this).parent("li").siblings('li').children("div").children("a").removeClass("on");
            if($(this).children("a").hasClass("on")){
                $(this).parent("li").parent("ul").siblings(".btn_red_wrap").removeClass('no');
            }            
        }
    });
}

//显示需要发票下的更多选项
function showAgreeMore(){
    if($("#btnNeed").hasClass('on') ){
        $("#btnNeed").parent("span").parent("div").siblings("div").show();
    }
}
//隐藏需要发票下的更多选项
function hideAgreeMore(){
    if($("#btnNeed:not([class='btn_agree on'])")){
        $("#btnNeed").parent("span").parent("div").siblings("div").hide();        
    }
}

//单选
function agreeRadio(){
    $("[data-agreeRadio]").each(function(){
        $(this).click(function(){
            if($(this).hasClass('on') ){
                $(this).parent("span").siblings("span").children("a").addClass("on");
            }else{
                $(this).parent("span").siblings("span").children("a").removeClass("on");
            }
        });
    });
    
}
//单选2
function agreeRadio2(){
    $("[data-agreeRadio2]").each(function(){
        $(this).click(function(){
            if($(this).hasClass('on') ){
                $(this).parent("span").parent("div").siblings("div").children('span').children("a[data-agreeRadio2]").addClass("on");
            }else{
                $(this).parent("span").parent("div").siblings("div").children('span').children("a[data-agreeRadio2]").removeClass("on");
            }
        });
    });
    
}
/*tab标题切换效果*/  
function doClick(o){
      o.className="nav_current";
      var j;
      var id;
      var e;
      for(var i=1;i<=3;i++){ //这里3 需要你修改 你多少条分类 就是多少
            id ="nav"+i;      
            j = document.getElementById(id);
            e = document.getElementById("sub"+i);
            if(id != o.id){
                  j.className="nav_link";
                  e.style.display = "none";
            }else{
               e.style.display = "block";
            }
      }
  }
//控制头部信息提示显示的时间
function tipsDelay(){
    $("[data-tips]").delay(600).fadeOut(400);
}

//控制btn_red_wrap按钮所在位置
/* function controlPosition(){
      var wHei=window.screen.height;
    if(wHei<=480){
        $("[data-getgray]").addClass("w_p_80");
        $("[data-getgray]").removeClass("btn_p_b");
    }else{
        $("[data-getgray]").removeClass("w_p_80");
        $("[data-getgray]").addClass("btn_p_b");
    }
 }*/
 //清除定位搜索输入框内的自问
$("[data-clearval]").click(function(){
    /*$(this).siblings("input").attr("value","");*/
    $("[data-inputbox]").hide();
    $("[data-select]").show();
    $("[data-sitesearch]").show();
    $("[ data-keyword]").hide();
    $("[data-level=1]").show();
});
function closeMarkBox(){
    $("[data-closemarkbox]").each(function(){
    $(this).click(function(){
        $(".mark_info").hide();
    });
});
}

//点击条目出现弹出层显示对应内容，以data-属性为查找器
function showMark(){
            var btnShowMark =$("a[data-showmarkbox]");
            var markBoxLi =$(".mark_info div[data-markbox]");
            btnShowMark.each(function(){
                $(this).click(function(){
                       if(btnShowMark.hasClass("no")){
                           return;
                       }
                       var thisData =$(this).data("showmarkbox");
                       for(var i=0;i<markBoxLi.length;i++){
                           $(markBoxLi[i]).hide();
                           var markBoxLiData =$(markBoxLi[i]).data("markbox");
                           if(thisData==markBoxLiData){
                               $(markBoxLi[i]).data("markbox",markBoxLiData).show();
                               $(markBoxLi[i]).data("markbox",markBoxLiData).parents(".mark_info").show();
                            }
                        }
        });
            });
}

//当定位滚动区域列表的内容超出父级高度时出现小箭头表示可以滚动看到更多
function aBtnMoreShow(){
    $("[data-conlists] ul").each(function(){
        var allHei=$(this).children().height()*$(this).children("li").length;
        var parentHei=$(this).height();
        var aBtnMore=$('<a href="javascript:void(0)" class="btn_more imgbox" data-btnmore>');
        var ImgBtnMore=$('<img src="../static/images/img_03.png" />').appendTo(aBtnMore);
        //创建向上箭头
        var aBtnMoreTop=$('<a href="javascript:void(0)" class="btn_moretop imgbox" data-btnmoretop>');
        var ImgBtnMoreTop=$('<img src="../static/images/img_03_2.png" />').appendTo(aBtnMoreTop);
        if(allHei>parentHei){
            aBtnMore.appendTo($(this));
            aBtnMoreTop.appendTo($(this));
            aBtnMore.show();
        }else{
            aBtnMore.remove();
            aBtnMoreTop.remove();
        }
    });
}
/*选择到餐时间*/
$("[data-selecttime]").each(function(){
    $(this).click(function(){
        $(this).siblings('ul').toggle();
        $(this).siblings('ul').children("li").each(function(){
            $(this).click(function(){
                $(this).parent("ul").siblings("a").children("span").html($(this).html());
                $(this).parent("ul").hide();
            });
        });
    });
});
