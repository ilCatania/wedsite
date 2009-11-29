var _blue = '#000066';
var _yellow = '#FFCC33';

var delta = 500;

var err = function() {
	alert("No response from server! Page will be reloaded.");
};

$.fn.mainNavFade = function() {
	return this.each(function() {
		var $$ = $(this);
		var $a = $$.find('a');
		$a.append("<div class='hover'>"+$a.text()+'</div>');
		var $div = $a.find('div');
		$$.hover(function() {
			$div.stop().fadeTo(0,1).fadeIn(delta);
		}, function() {
			$div.stop().fadeTo(0, 1).fadeOut(delta);
		});
	});
};

$.fn.subNavHover = function() {
	return this.each(function() {
		var $$ = $(this);
		var text = $$.text();
		var $div = $$.empty().append("<div class='hover'/>").find('div');
		$$.hover(function() {
			$$.stop();
			$div.stop().animate({paddingRight: '30px', width: '70px'}, delta/2, function() {
				$div.css({width: '170px'}).text(text);
				$$.animate({width: '200px'}, delta/2);
			});
		}, function() {
			$div.stop();
			$$.stop().animate({width: '100px'}, delta/2, function() {
				$div.empty().css({width: '70px'}).animate({paddingRight: '0', width: '0'}, delta/2);
			});
		});
	});
};


$.fn.selectLangButtons = function() {
	return this.each(function() {
		var $$ = $(this);
		var text = $$.text();
		var $div = $$.empty().append('<div/>').find('div');
		var $span = $('h2 .' + $$.attr('class'));
		$$.hover(function() {
			$div.stop().fadeTo(0,1).fadeIn(delta);
			$span.stop().fadeTo(0,1).fadeIn(delta);
		}, function() {
			$div.stop().fadeTo(0, 1).fadeOut(delta);
			$span.stop().fadeTo(0,1).fadeOut(delta);
		});
	});
};

$.fn.setupConfirmToggle = function() {
	return this.each(function() {
		var $form = $(this);
		var $p = $form.find('#addchildren');
		var $label = $form.find('#addchildren_label');
		var $input = $form.find('#id_children');
		var hideInput = function() {
			$input.val('');
			$input.hide();
			$label.hide();
			$p.show();
		};
		var showInput = function() {
			$input.show();
			$label.show();
			$p.hide();
		};
		$label.find('a').click(hideInput);
		$p.find('a').click(showInput);
		if($input.val())
			showInput();
		else
			hideInput();
	});
};

$.fn.setupEditConfirmationLink = function() {
	return this.each(function() {
		var $a = $(this);
		var id = $a.closest('li').attr('id').split('_').slice(1).join('_');
		var $form = $('#editconfirmation');
		$id_input = $form.find('input[name=edit_confirmation_id]');
		$a.click(function() {
			$id_input.val(id);
			$form.submit();
		});
	});
};

$.fn.setupDeleteConfirmationLink = function() {
	var $newConfirmationForm = $('#newconfirmation');
	var $maxConfirmationsReached = $('#maxconfirmations_message');
	return this.each(function() {
		var $a = $(this);
		var $li = $a.closest('li');
		var id = $li.attr('id').split('_').slice(1).join('_');
		$a.click(function() {
			$.post('.', {'delete': 'yes', 'edit_confirmation_id': id }, function(data){ 
				if(data) {
					$li.find('.body').text(data.message);
					$maxConfirmationsReached.fadeOut(delta);
					$newConfirmationForm.fadeIn(delta);
					setTimeout(function(){
						if(data.success)
						{
							$li.fadeOut(delta, function() {
								$li.remove();
								if($('#confirmations li').size() == 0)
									location.href = '.';
							});
						} else location.href = '.';
					}, 3000);
				} else {
					err();
					location.href = '.';
				}
			}, 'json');
		});
	});
};

$.fn.setupAjaxPollContent = function() {
	return this.each(function() {
		var $this = $(this);
		var last_hash = 'first_time_do_it_anyway';
		setInterval(function() {
			if(location.hash != last_hash) {
				var url = '';
				last_hash = location.hash;
				if(last_hash == '#answer') {
					url = 'form/';
				} else { //if(last_hash == '#results') {
					url = 'results/';
				} // else return;
				$.get(url, {}, function(data){
					if(data) $this.html(data);
					else err();
				}, 'html');
			}
		}, 50);
	});
};

$.fn.setupAjaxPollForm = function() {
	return this.each(function() {
		var $form = $(this);
		$form.ajaxForm({
			'target': '#ajax_poll',
			'error': function(resp) { 
				var text = resp.responseText.toString();
				if(text.length < 50)
					alert(text);
				else {
					; //TODO !
				}
			}
		});
	});
};

$.fn.marriageCountdown = function() {
	//TODO: UTC and GMT adjust
	var celebrationStart = new Date(2010, 1-1, 16, 11, 0, 0);
	var celebrationEnd = new Date(2010, 1-1, 16, 11, 0, 0);
	var now = new Date();

	var opts = {
		'format': 'yodhms', 
		'layout': 
			'<table>{y<}<tr><td class="col1"><strong>{yn}</td><td class="col2">{yl},</td></tr>{y>}' +
			'{o<}<tr><td class="col1">{on}</td><td class="col2">{ol},</td></tr>{o>}' +
			'{d<}<tr><td class="col1">{dn}</td><td class="col2">{dl},</td></tr>{d>}' +
			'{h<}<tr><td class="col1">{hn}</td><td class="col2">{hl},</td></tr>{h>}' +
			'{m<}<tr><td class="col1">{mn}</td><td class="col2">{ml} ' + gettext('and') +'</td></tr>{m>}' +
			'{s<}<tr><td class="col1">{sn}</td><td class="col2">{sl}{s>}</td></table>',
		'labels': [gettext('yy'), gettext('MM'), gettext('ww'),
		           gettext('dd'), gettext('HH'), gettext('mm'),
		           gettext('ss')], 
		'labels1': [gettext('yy1'), gettext('MM1'), gettext('ww1'),
		            gettext('dd1'), gettext('HH1'), gettext('mm1'),
		            gettext('ss1')]
	};

	var setCountdownContent = function(jq, text, options) {
		var $span = jq.html('<p>'+text+'</p>' +
				'<p>(<a href="javascript:void(0)" id="hide_countdown">' +
				gettext('hide_countdown') + '</a>)</p>'
				).find('span');
		$('#hide_countdown').click(function(){
			jq.empty().html('<p>(<a href="javascript:void(0)" id="show_countdown">' +
					gettext('show_countdown') + '</a>)</p>');
			$('#show_countdown').click(function(){
				jq.marriageCountdown();
			});
		});
		if(options) return $span.countdown(options);
		return $span;
	};
	
	var beforeCeremony = function(jq) {
		var text = gettext('getting_married_in') + ' <span></span>';
		var beforeOpts = $.extend({}, opts, {
			'until': celebrationStart,
			//timezone = +1,
			'onExpiry': function() { duringCeremony(jq); }
		});
		return setCountdownContent(jq, text, beforeOpts);
	};
	
	var duringCeremony = function(jq) {
		text = gettext('getting_married_now');
		var tId = setInterval(function() {
			if(new Date() > celebrationEnd) {
				clearInterval(tId);
				// afterCeremony(jq); does not work, dunno why.
				// ugly workaround: reload the page
				location.href = '.';
			}
		}, 1000);
		return setCountdownContent(jq, text);
	};
	
	var afterCeremony = function(jq) {
		var text = gettext('been_married_for') + ' <span></span>';
		var afterOpts = $.extend({}, opts, {
			'since': celebrationEnd/*,
			timezone = +1*/
		});
		setCountdownContent(jq, text, afterOpts);
	};
	
	if(now < celebrationStart) {
		beforeCeremony(this);
	} else if(now > celebrationEnd) {
		afterCeremony(this);
	} else {
		duringCeremony(this);
	}
};

$(document).ready(function() {
	$('#mainnav li:not(.selected)').mainNavFade();
	$('#subnav li:not(.selected) a').subNavHover();
	$('body.lang button').selectLangButtons();
	$('form#confirmparty').setupConfirmToggle();
	$('#confirmations .actions a.edit').setupEditConfirmationLink();
	$('#confirmations .actions a.delete').setupDeleteConfirmationLink();
	$('#ajax_poll').setupAjaxPollContent();
	$('#countdown').marriageCountdown();
});