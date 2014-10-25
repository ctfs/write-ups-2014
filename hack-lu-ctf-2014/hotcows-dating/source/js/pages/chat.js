page = (function() {
    page = Object.create(null);

    // class variables
    ctr = 0;
    cow_name = null;
    premium_id = null;
    has_premium = false;

    // all possible cow messages
    cowMessages = {
        'Rosie': [
            [function(m){return /asdf/i.test(m)}, "That's such an intelligent thing to say!"],
            [function(m){return /<[^ ].+>/.test(m)}, 'Good, you know how to do a basic XSS :))'],
            [function(m){return /bye/i.test(m)}, "Bye :'(("],
            [function(m){return /(^|[^\w])flag([^\w]|$)/i.test(m)}, "Oh, I don't know anything about a flag, but that stupid cow Maggie might..."],
            [function(){if(ctr==0){ctr++;return 1}}, "Hey there :))"],
            [function(){if(ctr==1){ctr++;return 1}}, "What's your name?"],
            [function(){if(ctr==2){ctr++;return 1}}, "I'm so lonely, you know..."],
            [function(){if(ctr==3){ctr++;return 1}}, "Just grazing the whole day. All by myself."],
            [function(){if(ctr==4){ctr++;return 1}}, "Do you want to be my cowboy?? :))"],
            [function(){if(ctr==5){ctr++;return 1}}, "Wait, I have some more pictures of me... do you want to see them??"],
            [function(){if(ctr==6){ctr++;return 1}}, function(){
                if (has_premium) {
                    return 'Yeah, well, ... right now the image server seems to be down, sorry...';
                } else {
                    return "Good, but sadly you need a PREMIUM acount for that :-// can't send it to you otherwise";
                }
            }],
        ],
        'Clara': [
            [function(m){return /bye/i.test(m)}, "Bye, come back soon :**"],
            [function(m){return /(^|[^\w])flag([^\w]|$)/i.test(m)}, "I don't know and I don't care about flags."],
            [function(){if(ctr==0){ctr++;return 1}}, "Oooops, are you looking at my udder?"],
            [function(){if(ctr==1){ctr++;return 1}}, "All other cows tell me it's small. What do you think?"],
            [function(){if(ctr==2){ctr++;return 1}}, "On a scale of 1-10, where 10 is best... how would you rate it?"],
            [function(){if(ctr==3){ctr++;return 1}}, "Are you sure???"],
            [function(){if(ctr==4){ctr++;return 1}}, "Really?"],
            [function(){if(ctr==5){ctr++;return 1}}, "Don't be silly, please."],
            [function(){if(ctr==6){ctr++;return 1}}, "I really feel like it's lacking in comparison to other cows."],
            [function(){if(ctr==7){ctr++;return 1}}, "Maybe I need a plastic surgery..."],
            [function(){if(ctr==8){ctr++;return 1}}, "Would you pay for that? Please??"],
            [function(){if(ctr==9){ctr++;return 1}}, function() {
                if (has_premium) {
                    return "Just send your credit card details to premium@hotcows.xxx please";
                } else {
                    return "Having a PREMIUM membership would greatly help... just saying...";
                }
            }],
        ],
        'Maggie': [
            [function(m){return /bye/i.test(m)}, "Where are you going? Are you leaving me alone??"],
            [function(m){return /(^|[^\w])flag($|[^\w])/i.test(m)}, "Yes, I've overheard that Abbie might know something about that. But you'll stay here, don't you?"],
            [function(){if(ctr==0){ctr++;return 1}}, "Howdy cowboy!"],
            [function(){if(ctr==1){ctr++;return 1}}, "I'm Maggie and I think I am already falling in deep eternal love with you..."],
            [function(){if(ctr==2){ctr++;return 1}}, "Would you marry me?"],
            [function(){if(ctr==3){ctr++;return 1}}, "Not trying to overwhelm you here, but I kinda feel unsafe alone."],
            [function(){if(ctr==4){ctr++;return 1}}, "Wait, what was that noise? I'll just quickly check that."],
            [function(){if(ctr==5){ctr++;return 1}}, "Oooh, I need a protector sooo much..."],
            [function(){if(ctr==6){ctr++;return 1}}, "How about I give you my address and you come over?"],
            [function(){if(ctr==7){ctr++;return 1}}, function(){
                if (has_premium) {
                    return "Nevermind, I have to go now! Will be back in some hours.";
                } else {
                    return "Sorry, I have been advised to not trust people without a PREMIUM membership :-/";
                }
            }],
        ],
        'Abbie': [
            [function(m){return /bye/i.test(m)}, "Yes, yes, leave an old cow to herself..."],
            [function(m){return /(^|[^\w])flag($|[^\w])/i.test(m)}, function() {
                if (has_premium) {
                    return 'Yes, the secret is that the PREMIUM ID is actually the flag :)';
                } else {
                    return 'Sorry, I will only tell secrets to PREMIUM members. Send your bank details to premium@hotcows.xxx, honey, and I will immediately tell you about this flag :**';
                }
            }],
            [function(){if(ctr==0){ctr++;return 1}}, 'Hello stranger'],
            [function(){if(ctr==1){ctr++;return 1}}, 'You know, I might be old, but I have got some really nice hooves.'],
            [function(){if(ctr==2){ctr++;return 1}}, 'I hope you\'re into hooves.'],
            [function(){if(ctr==3){ctr++;return 1}}, 'Sooo, mine are a little dirty in this picture, but maybe you like that, too?'],
            [function(){if(ctr==4){ctr++;return 1}}, 'I know that you do ;)'],
            [function(){if(ctr==5){ctr++;return 1}}, 'Now I\'ll leave you to your dirty fantasies and moo a bit, okay?'],
        ],
    };

    /**
     * Finds a chat answer based on the message of the user and the current
     * cow's name.
     */
    page.chatAnswer = function chatAnswer(msg, cow_name) {
        if (cowMessages.hasOwnProperty(cow_name)) {
            for (i = 0; i < cowMessages[cow_name].length; i++) {
                if (cowMessages[cow_name][i][0](msg)) {
                    return page.getMessage(cowMessages[cow_name][i][1]);
                }
            }
        }
        traits = ['gnarly', 'sexy', 'erotic', 'erotique', 'lovely', 'horny',
                  'soft', 'tender', 'severe', 'eloquent'];
        return '*' + traits[Math.floor(Math.random() * traits.length)] + ' moo*';
    };

    /**
     * Appends a message to the main chat.
     */
    page.appendMessage = function appendMessage(temp) {
        output = temp.renderToString();
        (chat = document.getElementById('mainchat')).innerHTML += output;
        chat.scrollTop = chat.scrollHeight;
    };

    /**
     * Since chat answers can be strings or functions: This function finds out
     * the correct type and returns a string.
     */
    page.getMessage = function getMessage(string_or_function) {
        if (typeof string_or_function == 'function') {
            return string_or_function();
        }
        return string_or_function;
    }

    /**
     * Obtain PREMIUM status and PREMIUM ID.
     */
    page.getPremium = function getPremium() {
        return form.parseJSON(http.get('?api=premium.php', undefined, undefined, true));
    };

    /**
     * View function. Externally called.
     */
    page.view = function view() {
        cow_name = location.hash.slice(1);
        if (!cow_name) {
            return router.route('error');
        }
        premium = page.getPremium();
        has_premium = premium['success'];
        premium_id = premium['message'];

        temp_main = new Template('cow.html');
        temp_main.assign(cow_name, 'cow');
        temp_main.render();
        btn_logout = document.getElementById('btn-logout');
        if (!!btn_logout) {
            btn_logout.onclick = function _logout() {
                router.route('logout');
            };
        }
        btn_overview = document.getElementById('btn-overview');
        if (!!btn_overview) {
            btn_overview.onclick = function _back() {
                router.route('internal');
            };
        }
        btn_report = document.getElementById('btn-report');
        if (!!btn_report) {
            btn_report.onclick = function _report() {
                router.route('report');
            };
        }

        temp = new Template('message.html');
        chatform = document.getElementById('chatform');
        if (!!chatform) {
            chatform.onsubmit = function _chat(e) {
                e.preventDefault();
                if (!!e.target.msg.value) {
                    // append user's chat message
                    temp.assign('me', 'class');
                    temp.assign('Me', 'name')
                    temp.assign(e.target.msg.value, 'msg');
                    page.appendMessage(temp);

                    // append cow's answer
                    temp.assign('her', 'class');
                    temp.assign(cow_name, 'name')
                    temp.assign(page.chatAnswer(e.target.msg.value, cow_name),
                                'msg');
                    page.appendMessage(temp);

                    // reset input field
                    e.target.reset();
                }
            };
        }

        Array.prototype.forEach.call(
            document.querySelectorAll('.premium'),
            function _mailPremium(node) {
                node.onclick = function _startMailApp() {
                    showAlert('Send a mail to premium@hotcows.xxx with your bank details and account name.');
                }
            }
        );
    };

    /**
     * Greet the user after a while to avoid suspicion.
     */
    page.firstMessage = function firstMessage() {
        if (!!temp) {  // if template loaded
            temp.assign('system', 'class');
            temp.assign('In chat with', 'name')
            message = cow_name + ((has_premium) ? ' (' + premium_id + ')' : '');
            temp.assign(message, 'msg');
            page.appendMessage(temp);
            temp.assign('her', 'class');
            temp.assign(cow_name, 'name')
            temp.assign(page.chatAnswer('', cow_name), 'msg');
            page.appendMessage(temp);
        } else {
            // wait some more
            setTimeout(page.firstMessage, 1000);
        }
    };

    return page;
})();


setTimeout(page.firstMessage, 1000);
