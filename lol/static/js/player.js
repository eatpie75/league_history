(function(){var ChampionSort,PlayerGamePageHandler,StatFilter;PlayerGamePageHandler=function(){function PlayerGamePageHandler(){this.page=1,this.summoner=window.account_id,this._bind()}return PlayerGamePageHandler.prototype._bind=function(){var _this_;return _this_=this,$(".page_link").bind("click",function(e){return _this_.change_page($(this))}),window.connect_items()},PlayerGamePageHandler.prototype.change_page=function(el){var page,_this=this;return el==null&&(el=1),typeof el=="object"?page=el.data("page"):page=el,$.ajax({type:"GET",url:"/ajax/summoner_games/"+this.summoner+"/?page="+page,dataType:"html",success:function(msg){return $("#games").html(msg),_this._bind()}})},PlayerGamePageHandler}(),ChampionSort=function(){function ChampionSort(){this.direction=1,this.column=$(".table-sort.active:first"),this.column_str=this.column.data("column"),this.icon=this.column.children("span").children("i"),this._icons={"-1":"icon-arrow-up",1:"icon-arrow-down"},this._bind()}return ChampionSort.prototype._bind=function(){var _this_;return _this_=this,$(".table-sort").bind("click",function(e){var el;return el=$(this),_this_.column_str===el.data("column")?(_this_.icon.removeClass(_this_._icons[""+_this_.direction]).addClass(_this_._icons[""+_this_.direction*-1]),_this_.direction*=-1):(_this_.column.removeClass("active"),_this_.icon.removeClass(_this_._icons[""+_this_.direction]),_this_.direction=1,_this_.column=el,_this_.column_str=_this_.column.data("column"),_this_.icon=_this_.column.children("span").children("i"),_this_.column.addClass("active"),_this_.icon.addClass(_this_._icons[""+_this_.direction])),_this_.sort(el.data("column"))})},ChampionSort.prototype.sort=function(column){var _sort,_this=this;return _sort=function(a,b){var c,d,pregex,_ref,_ref1;return pregex=new RegExp("(\\d+)%","i"),c=$(a).children("."+column).text(),d=$(b).children("."+column).text(),!isNaN(Number(c))&&!isNaN(Number(d))?(_ref=[Number(c),Number(d)],c=_ref[0],d=_ref[1],c>d?-1*_this.direction:c===d?0:1*_this.direction):pregex.test(c)&&pregex.test(d)?(_ref1=[Number(c.match(pregex)[1]),Number(d.match(pregex)[1])],c=_ref1[0],d=_ref1[1],c>d?-1*_this.direction:c===d?0:1*_this.direction):c>d?1*_this.direction:c===d?0:-1*_this.direction},$(".cbody").append($(".cbody .sort").sort(_sort)),this.current_column=column},ChampionSort}(),StatFilter=function(){function StatFilter(){this._bind()}return StatFilter.prototype._bind=function(){var _this_;return _this_=this,$("#stat-filter").bind("change",function(){return $("#stat-filter").submit()})},StatFilter}(),$(document).ready(function(){return window.page_handler=new PlayerGamePageHandler,window.champion_sort=new ChampionSort,window.stat_filter=new StatFilter})}).call(this)