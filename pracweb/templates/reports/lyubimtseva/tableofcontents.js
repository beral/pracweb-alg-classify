(function( $ ){

  $.fn.tableofcontents = function() {
	    var toc=this;
		var p1=0;
		var p2=0;
		var p3=0;
		var p4=0;
		toc.html('');
		$('h1, h2, h3,h4').each(function(){
			$(this).attr('tag',this.nodeName.toLowerCase());
			if($(this).attr('tag')=='h1')
			{
				p2=0;p3=0;p1=p1+1;p4=0;
				toc.html(toc.html()+'<span class="toc1"><a href="#S'+p1+'">'+p1+'. '+ $(this).html()+'</a></span><br/>');
				$(this).html('<a name="S'+p1+'"</a>'+p1+'. '+ $(this).html());
					
			}
			if($(this).attr('tag')=='h2')
			{
				p3=0;p2=p2+1;p4=0;
				toc.html(toc.html()+'<span class="toc2"><a href="#S'+p1+'_'+p2+'">'+p1+'.'+p2+'. '+ $(this).html()+'</a></span><br/>');
				$(this).html('<a name="S'+p1+'_'+p2+'"></a>'+p1+'.'+p2+'. '+ $(this).html());
				
			}
			if($(this).attr('tag')=='h3')
			{
				p3=p3+1;p4=0;
				toc.html(toc.html()+'<span class="toc3"><a href="#S'+p1+'_'+p2+'_'+p3+'">'+p1+'.'+p2+'.'+p3+'. '+ $(this).html()+'</a></span><br/>');
				$(this).html('<a name="S'+p1+'_'+p2+'_'+p3+'"></a>'+p1+'.'+p2+'.'+p3+'. '+ $(this).html());
			}
			if($(this).attr('tag')=='h4')
			{
				p4=p4+1;
				toc.html(toc.html()+'<span class="toc4"><a href="#S'+p1+'_'+p2+'_'+p3+'_'+p4+'">'+p1+'.'+p2+'.'+p3+'.'+p4+'. '+ $(this).html()+'</a></span><br/>');
				$(this).html('<a name="S'+p1+'_'+p2+'_'+p3+'_'+p4+'"></a>'+p1+'.'+p2+'.'+p3+'.'+p4+'. '+ $(this).html());
			}

		});
		
    };

})( jQuery );

