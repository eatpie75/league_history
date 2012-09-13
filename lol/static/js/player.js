(function(){var e,t,n,r,i,s;t=function(){function e(){this.page=1,this.account_id=window.account_id,this.region=window.region,this._bind()}return e.prototype._bind=function(){var e;return e=this,$(".page_link").bind("click",function(t){return e.change_page($(this))}),window.connect_items()},e.prototype.change_page=function(e){var t,n=this;return e==null&&(e=1),typeof e=="object"?t=e.data("page"):t=e,$.ajax({type:"GET",url:""+window.AJAX_BASE+"ajax/summoner_games/"+this.region+"/"+this.account_id+"/?page="+t,dataType:"html",success:function(e){return $("#games").html(e),n._bind()}})},e}(),e=function(){function e(){var e;this.column=$(".table-sort.active:first"),this.column.length>0&&(this.column_str=this.column.data("column"),this.direction=1,this.icon=this.column.children("span").children("i"),this._icons={"-1":"icon-arrow-up",1:"icon-arrow-down"},this._bind(),e=s(window.location.hash.slice(1)),"sort"in e&&("direction"in e&&(this.direction=Number(e.direction)),this.change($(".table-sort").filter(function(t){return $(this).data("column")===e.sort}).first(),!0)))}return e.prototype._bind=function(){var e;return e=this,$(".table-sort").bind("click",function(t){return e.change($(this))})},e.prototype.change=function(e,t){var n;return t==null&&(t=!1),t&&this.icon.removeClass(this._icons[1]),this.column_str===e.data("column")?(this.icon.removeClass(this._icons[""+this.direction]).addClass(this._icons[""+this.direction*-1]),this.direction*=-1):(this.column.removeClass("active"),this.icon.removeClass(this._icons[""+this.direction]),t===!1&&(this.direction=1),this.column=e,this.column_str=this.column.data("column"),this.icon=this.column.children("span").children("i"),this.column.addClass("active"),this.icon.addClass(this._icons[""+this.direction])),this.sort(e.data("column"),e.data("spec-order")),n=s(window.location.hash.slice(1)),n.sort=e.data("column"),this.direction===-1?n.direction=this.direction:delete n.direction,window.location.hash=$.param(n)},e.prototype.sort=function(e,t){var n,r,i,s=this;return t==null&&(t=null),n=new RegExp("(\\d+)%","i"),r=function(e,t,n,r){return e>t?-1*s.direction:e===t?n>r?-1*s.direction:1*s.direction:1*s.direction},i=function(i,o){var u,a,f,l,c,h,p,d,v,m;return p=[$(i),$(o)],i=p[0],o=p[1],c=i.children("."+e).text(),h=o.children("."+e).text(),t!=null&&t==="swin"?(d=[Number(c.match(n)[1]),Number(h.match(n)[1])],c=d[0],h=d[1],a=Math.round(window.num_games*.04),u=Math.round(window.num_games*.01),f=Number(i.children(".total").text()),l=Number(o.children(".total").text()),f>=a?l>=a?r(c,h,f,l):-1*s.direction:l>=a?1*s.direction:f>=u?l>=u?r(c,h,f,l):-1*s.direction:r(c,h,f,l)):!isNaN(Number(c))&&!isNaN(Number(h))?(v=[Number(c),Number(h)],c=v[0],h=v[1],c>h?-1*s.direction:c===h?0:1*s.direction):n.test(c)&&n.test(h)?(m=[Number(c.match(n)[1]),Number(h.match(n)[1])],c=m[0],h=m[1],c>h?-1*s.direction:c===h?0:1*s.direction):c>h?1*s.direction:c===h?0:-1*s.direction},$(".cbody").append($(".cbody .sort").sort(i)),this.current_column=e},e}(),n=function(){function e(){this._bind()}return e.prototype._bind=function(){var e;return e=this,$("#stat-filter").bind("change",function(){var e,t;return e=$(this),t={},e.children("#id_game_map").val()!=="-1"&&(t.game_map=e.children("#id_game_map").val()),e.children("#id_game_mode").val()!=="-1"&&(t.game_mode=e.children("#id_game_mode").val()),window.location.search=$.param(t)})},e}(),s=function(e){var t,n,r,i,s;e=e.split("&"),r={};for(i=0,s=e.length;i<s;i++){n=e[i],t=n.split("=");if(t[0]===""&&t.length===1)break;r[decodeURI(t[0])]=decodeURI(t[1])}return r},i=function(e){var t,n=this;return t=function(){var e=this;return $.ajax({type:"GET",url:""+window.AJAX_BASE+"ajax/force_update_status/"+window.region+"/"+window.account_id+"/",dataType:"json",success:function(e){if(e.status==="QUEUE")return setTimeout(t,e.delay);if(e.status==="DONE")return $("#last-updated").text(e.msg)}})},$("#last-updated-block").html("<small id='last-updated'>WORKING...</small>"),$.ajax({type:"GET",url:""+window.AJAX_BASE+"ajax/force_update/"+window.region+"/"+window.account_id+"/",dataType:"json",success:function(e){$("#last-updated").text("LAST UPDATED:"+e.msg);if(e.status==="QUEUE")return setTimeout(t,e.delay)}})},r=function(e,t,n,r){var i,s,o,u,a,f,l,c,h,p,d,v,m;t==null&&(t="rating"),n==null&&(n={}),r==null&&(r="default"),i=document.getElementById("elo-graph"),u={xaxis:{mode:"time",showLabels:!1},yaxis:{autoscale:!0,autoscaleMargin:1,showLabels:!1,tickFormatter:function(e){return""+e+"%"}},mouse:{track:!0,trackFormatter:function(e){return""+Flotr.Date.format(e.x,"%y-%m-%d")+": "+Math.round(e.y)},sensiblility:3,lineColor:"#fff",relative:!0},lines:{fill:!0,show:!0},points:{show:!0,lineWidth:1,radius:2,fillColor:"#00A8F0"},grid:{color:"#fff",verticalLines:!1,horizontalLines:!1,outline:""}},f=$.extend({},u),$.extend(!0,f,n);if(r==="default"){l=[];for(c=0,d=e.length;c<d;c++){o=e[c];if(o[1][t]<10)continue;l.push([new Date(o[0]),o[1][t]])}}else if(r==="chistorywr"){l=[];for(h=0,v=e.length;h<v;h++){o=e[h],s=new Date(o[0]),a=new Date;if(o[1].champions[t].count<10)continue;l.push([s,o[1].champions[t].won/o[1].champions[t].count*100])}}else if(r==="chistorypop"){l=[];for(p=0,m=e.length;p<m;p++){o=e[p];if(o[1].champions[t].count<10)continue;l.push([new Date(o[0]),o[1].champions[t].won/o[1].count*100])}}return Flotr.draw(i,[l],f)},$(document).ready(function(){return window.page_handler=new t,window.champion_sort=new e,window.stat_filter=new n,window.draw_chart=r,$("#force-update").bind("click",i),window.bgchart!=null&&r(window.data,window.bgchart),$('a[data-toggle="tab"]').click(function(e){return e.preventDefault(),$(this).tab("show")})})}).call(this)