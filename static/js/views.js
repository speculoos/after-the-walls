/*
 * 
 * ATW.views.js
 * 
 */

(function(undefined){
    'strict';
    var ATW = window.ATW;
    
    ATW.LogWidget = Backbone.View.extend({
        className:'log-widget widget',
        initialize:function(isLogged){
            this.isLogged = isLogged;
        },
        render:function(){
            var $el = this.$el;
            $el.empty();
            var data = {logged:ATW.Config.user_name !== undefined};
            Template.render('log-widget', this, function(t){
                var h = t(data);
                $el.html(h);
            });
            return this;
        },
        open:function(){
            
        },
        close:function(){
            
        },
        login:function(){
            
        },
        logout:function(){
            
        },
    });
    
    ATW.ContactWidget = Backbone.View.extend({
        className:'contact-widget widget',
        initialize:function(isLogged){
            this.isLogged = isLogged;
        },
        render:function(){
            var $el = this.$el;
            $el.empty();
            var data = {logged:this.isLogged};
            Template.render('contact-widget', this, function(t){
                $el.html(t(data));
            });
            return this;
        },
        open:function(){
            
        },
        close:function(){
            
        },
        send:function(){
            
        },
    });
    
    ATW.RegisterWidget = Backbone.View.extend({
        className:'register-widget widget',
        initialize:function(isLogged){
            this.isLogged = isLogged;
        },
        render:function(){
            var $el = this.$el;
            $el.empty();
            var data = {logged:this.isLogged};
            Template.render('register-widget', this, function(t){
                $el.html(t(data));
            });
            return this;
        },
        open:function(){
            
        },
        close:function(){
            
        },
        send:function(){
            
        },
    });
    
    ATW.VideoPlayer = Backbone.View.extend({
        id:'video-player',
        initialize:function(){
            this.playerReady = false;
            
        },
        render:function(){
            var $el = this.$el;
            $el.empty();
            Template.render('video-player', this, function(t){
                $el.html(t({}));
                this.player = $el.find('.player');
                this.controls = $el.find('.controls');
                this.playerReady = true;
            });
            return this;
        },
        loadMedia:function(item){
            if(!this.playerReady)
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
            var options = {
                timeupdate: this.update.bind(this),
                cssSelectorAncestor: '#'+$el.attr('id'),
                errorAlerts: true,
                warningAlerts: false,
                swfPath: "./lib/Jplayer.swf",
                supplied: type,
            };
            this.player.jPlayer(options);
            var media = {};
            media[type] = item.get('resource');
            this.player.jPlayer('setMedia', media);
        },
        update:function(){
            
        },
        play:function(){
            this.player.jPlayer('play');
        },
        pause:function(){
            
        },
        playHead:function(){
            
        },
        louder:function(){
            
        },
        softer:function(){
            
        },
        mute:function(){
            
        },
    });
})();
