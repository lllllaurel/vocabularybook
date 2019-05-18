$(document).ready(function(){
	$.get('/getword/',{cnt:0},function(data){
		wordObj = data;
		for (var i = 0; i <data['ch'].length; i++) {
			$('#bb-show').append("<div style='display:none'>"+data['ch'][i]+"</div>");
		}
		$("#bb-show").children(":first").css('display','block');
		$("#bb-show").children(":first").attr('id','show');
	});
	$("button").click(function(){
		var cnt = $('#blackboard').attr('myAttr');
		cnt = parseInt(cnt);
		cnt++;
		if (wordObj['ch'].length<20&&cnt%20==wordObj['ch'].length)  {
			alert('last word!');
			return false;
		}
		if (cnt%20==0) {
			$.get('/getword/',{cnt:cnt},function(data){
				wordObj=data;
				$("#bb-show").children().remove();
				for (var i = 0; i <data['ch'].length; i++) {
					$('#bb-show').append("<div style='display:none'>"+data['ch'][i]+"</div>");
				}
				$("#bb-show").children(":first").css('display','block');
				$("#bb-show").children(":first").attr('id','show');
			});
		}
		var cnt_s = cnt.toString();
		var cnt = $('#blackboard').attr('myAttr',cnt_s);
		var obj = $('#show').next();
		$('#show').css('display','none');
		$('#show').removeAttr('id');
		
		obj.attr('id','show');
		obj.css('display','block');
	})
})