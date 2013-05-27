/*
 * 
 * ATW.views.js
 * 
 */

(function(undefined){
    'strict';
    var ATW = window.ATW;
    
    
    ATW.AlertView = Backbone.View.extend({
        className:'alert',
        initialize:function(){
            this.$close = $('<button>&times;</button>').addClass('close'); 
            if(this.options.status)
            {
                this.$el.addClass('alert-'+this.options.status);
            }
        },
        render:function(){
            this.$close.appendTo(this.el);
            this.$el.append(this.options.message || 'ERROR happened');
            return this;
        },
        events:{
            'click .close':'close',
        },
        close:function(){
            this.trigger('close');
            this.$el.remove();
        }
        
    });
    
    ATW.HTMLEpisodeview = Backbone.View.extend({
        className:'html-widget',
        initialize:function(){
            
        },
        render:function(){
            var $el = this.$el;
            $el.empty();
//             var data = this.model.toJSON();
//             Template.render('html-widget', this, function(t){
//                 $el.html(t(data));
            //             });
            this.$el.html(this.model.get('body'));
            if(this.model.get('bg_image'))
            {
                if(this.proxyView)
                {
                    if(this.proxyView.$el.data('backstretch') !== undefined)
                        this.proxyView.$el.data('backstretch').destroy();
                    this.proxyView.$el.backstretch(this.model.get('bg_image'));
                }
                else
                    this.$el.backstretch(this.model.get('bg_image'));
            }
            return this;
        },
    });
    
    ATW.LogWidget = Backbone.View.extend({
        className:'log-widget',
        initialize:function(){
        },
        render:function(){
            var $el = this.$el;
            $el.empty();
            var data = {logged:app.isLogged()};
            Template.render('log-widget', this, function(t){
                var h = t(data);
                $el.html(h);
            });
            return this;
        },
        events:{
            'click .login .submit': 'login',
        },
        _login_success:function(data){
            if(data.error)
            {
//                 console.log('Login Error: '+data.error);
                return;
            }
            _.extend(ATW.Config, data);
            app.profiles.fetch({reset:true});
            app.resetViews(['login','contact']);
            router.navigate('visit');
        },
        _login_error:function(response){
            var data = JSON.parse(response.responseText);
            var alert = new ATW.AlertView({
                message:data.error,
                status:'error',
            })
            this.$el.append(alert.render().el);
        },
        login:function(){
            var user = this.$el.find('input.user').val();
            var key = this.$el.find('input.key').val();
            $.ajax({
                type: "POST",
                url: '/login',
                data: { user:user, key:key },
                success: this._login_success.bind(this),
                error: this._login_error.bind(this),
                dataType: 'json'
            });
        },
    });
    
    ATW.NavBar = Backbone.View.extend({
        className:'nav-bar',
        render:function(){
            var $el = this.$el;
            $el.empty();
            var data = {logged:app.isLogged()};
            Template.render('nav-bar', this, function(t){
                $el.html(t(data));
            });
            return this;
        },
    });
    
    ATW.ContactWidget = Backbone.View.extend({
        className:'contact-widget',
        initialize:function(){
        },
        render:function(){
            var $el = this.$el;
            $el.empty();
            var data = {logged:app.isLogged()};
            Template.render('contact-widget', this, function(t){
                $el.html(t(data));
            });
            return this;
        },
        events:{
            'click .submit': 'send',
        },
        send:function(){
            var subject = this.$el.find('input.subject').val();
            var body = this.$el.find('textarea.text').val();
            app.saveMessage(subject, body);
        },
    });
    
    ATW.RegisterWidget = Backbone.View.extend({
        className:'register-widget hero-unit',
        initialize:function(){
        },
        render:function(){
            var $el = this.$el;
            $el.empty();
            var data = {logged:app.isLogged()};
            Template.render('register-widget', this, function(t){
                $el.html(t(data));
                $el.find('.answer').hide();
            });
            return this;
        },
        events:{
            'click .form .submit': 'send',
        },
        _register_success:function(data){
            var form = this.$el.find('.form');
            var success = this.$el.find('.answer');
            form.empty().append(success);
            success.show();
        },
        _register_error:function(response){
            var data = JSON.parse(response.responseText);
            var alert = new ATW.AlertView({
                message:data.error,
                status:'error',
            })
            this.$el.append(alert.render().el);
        },
        send:function(){
            var name = this.$el.find('input.name').val();
            var mail = this.$el.find('input.mail').val();
            $.ajax({
                type: "POST",
                url: '/register_step_0',
                data: { name:name, email:mail},
                success: this._register_success.bind(this),
                error: this._register_error.bind(this),
                dataType: 'json'
            });
        },
    });
    
    ATW.VideoPlayer = Backbone.View.extend({
        id:'video-player',
        initialize:function(){
            this._playerRendered = false;
            
        },
        render:function(){
            var $el = this.$el;
            $el.empty();
            Template.render('video-player', this, function(t){
                $el.html(t({}));
                this.player = $el.find('.player');
                this.controls = $el.find('.controls');
                this._playerRendered = true;
            });
            return this;
        },
        loadMedia:function(item){
            if(!this._playerRendered)
            {
                var self = this;
                window.setTimeout(function(){
                    self.loadMedia(item);
                }, 500);
                return;
            }
            var $el = this.$el;
            this.player.jPlayer("destroy");
            var type = item.get('mime').split('/').pop();
            var self = this;
            
            var media = {};
            media[type] = item.get('resource');
            var options = {
                ready:function(){
                    self.player.jPlayer('setMedia', media);
                    self.trigger('player:ready');
                },
                timeupdate: this.update.bind(this),
                cssSelectorAncestor: '#'+$el.attr('id'),
                errorAlerts: false,
                warningAlerts: false,
                swfPath: "/static/lib/Jplayer.swf",
                supplied: type,
                fullWindow:true,
            };
            this.player.jPlayer(options);
            this._playerRendered = false;
        },
        update:function(){
            
        },
        play:function(){
            this.player.jPlayer('play');
        },
        pause:function(){
            this.player.jPlayer('pause');
        },
    });
    
    ATW.AudioPlayer = Backbone.View.extend({
        id:'audio-player',
        initialize:function(){
            this._playerRendered = false;
            
        },
        render:function(){
            var $el = this.$el;
            $el.empty();
            Template.render('audio-player', this, function(t){
                $el.html(t({}));
                this.player = $el.find('.player');
                this.controls = $el.find('.controls');
                this._playerRendered = true;
            });
            return this;
        },
        loadMedia:function(item){
            if(!this._playerRendered)
            {
                var self = this;
                window.setTimeout(function(){
                    self.loadMedia(item);
                }, 500);
                return;
            }
            var $el = this.$el;
            this.player.jPlayer("destroy");
            var self = this;
            var type = item.split('.').pop();
            
            var media = {};
            media[type] = item;
            var options = {
                ready:function(){
                    self.player.jPlayer('setMedia', media);
                    self.trigger('player:ready');
                },
                timeupdate: this.update.bind(this),
                cssSelectorAncestor: '#'+$el.attr('id'),
                errorAlerts: false,
                warningAlerts: false,
                swfPath: "/static/js/lib/Jplayer.swf",
                supplied: type,
                loop:true,
            };
            this.player.jPlayer(options);
            this.playerData = this.player.data('jPlayer');
            this._playerRendered = false;
        },
        update:function(){
            
        },
        play:function(){
            this.player.jPlayer('play');
        },
        pause:function(){
            this.player.jPlayer('pause');
        },
        events:{
            'click .volume-down':'volDown',
            'click .volume-up':'volUp',
        },
        volDown:function(){
            this.player.jPlayer('volume', this.playerData.options.volume - .1);
        },
        volUp:function(){
            this.player.jPlayer('volume', this.playerData.options.volume + .1);
        },
    });
})();
