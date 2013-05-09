/*
 * 
 * ATW.app.js
 * 
 */


(function(undefined){
    'strict';
    
    var EpisodeProto = {
        events:{
            'click':'play',
        },
        play:function(){
            window.router.navigate('episode/'+this.model.id);
        },
    };
    
    var HomeView =  Backbone.View.extend({
        id:'galery',
        initialize:function(){
            this.images = new window.ATW.Collections.homeimage;
            this.images.on('add', this.renderOne, this);
            this.images.on('reset', this.render, this);
        },
        initBack:function(item){
            this.$el.backstretch(item.get('image'), {fade:'slow'});
            this.backstretch = this.$el.data('backstretch');
        },
        renderOne:function(item){
            if(this.backstretch === undefined)
                this.initBack(item);
            else
                this.backstretch.images.push(item.get('image'));
            return this;
        },
        render:function(){
            this.images.each(function(item){
                this.renderOne(item);
            }, this);
            return this;
        },
        next:function(){
            
        },
    });
    
    var EpisodeCollectionView = Backbone.View.extend({
        id:'episodes',
        initialize:function(){
            this.episodes = new window.ATW.Collections.episode;
            this.episodes.on('add', this.renderOne, this);
            this.episodes.on('reset', this.render, this);
            this.items = {};
        },
        renderOne:function(item){
            if(this.items[item.cid] === undefined)
            {
                item.set({
                    visited:false,
                    current:false,
                });
                var i = new window.ATW.Views.episode({model:item});
                this.$el.append(i.render().el);
                this.items[item.cid] = i;
            }
            return this;
        },
        render:function(){
            this.episodes.each(function(item){
                this.renderOne(item);
            }, this);
            return this;
        },
    });
    
    
    
    var AppView =  Backbone.View.extend({
        el:'body',
        initialize:function(){
            this.components = {};
            window.ATW.Modeler(function(){
//                 _.extend(window.ATW.Views.homeimage.prototype, ImageProto);
                _.extend(window.ATW.Views.episode.prototype, EpisodeProto);
                
                this.medias = new ATW.Collections.media;
                this.medias.fetch();
                
                this.components.home = {
                    view: new HomeView,
                    visible: false,
                    rendered: false,
                };
                this.components.episodes = {
                    view:new EpisodeCollectionView,
                    visible:false,
                    rendered: false,
                };
                this.components.login = {
                    view:new ATW.LogWidget,
                    visible:false,
                    rendered: false,
                };
                this.components.register = {
                    view:new ATW.RegisterWidget,
                    visible:false,
                    rendered: false,
                };
                this.components.player = {
                    view:new ATW.VideoPlayer,
                    visible:false,
                    rendered: false,
                };
                this.components.visit = {
                    view:new ATW.VisitWidget,
                    visible:false,
                    rendered: false,
                };
                this.components.contact = {
                    view:new ATW.ContactWidget,
                    visible:false,
                    rendered: false,
                };
                
                this.components.home.view.images.fetch();
                this.components.episodes.view.episodes.fetch();
                this.episodes = this.components.episodes.view.episodes;
                
                this.messages = new ATW.Collections.message;
                
                this.trigger('ready');
            }, this);
        },
        render:function(){
            for(var k in this.components){
                var c = this.components[k];
                if(c.visible)
                {
                    this.$el.append(c.view.el);
                    if(!c.rendered)
                    {
                        c.view.render();
                        c.rendered = true;
                    }
                }
            }
        },
        resetViews:function(comps){
            for(var i=0; i<comps.length; i++)
            {
                var c = comps[i];
                try{
                    this.components[c].rendered = false;
                }
                catch(e){
                    console.log('Could not reset: '+c);
                }
            }
            this.render();
        },
        setComponents:function(comps){
            for(var k in this.components){
                var c = this.components[k];
                c.visible = false;
                c.view.$el.detach();
            }
            for(var i=0; i<comps.length; i++)
            {
                var c = comps[i];
                try{
                    this.components[c].visible = true;
                }
                catch(e){
                    console.log('Could not activate: '+c);
                }
            }
            this.render();
        },
        isLogged:function(){
            if(ATW.Config.user_name !== 'AnonymousUser'
                && ATW.Config.user_name !== undefined
                && ATW.Config.api_key !== undefined )
                return true;
            return false;
        },
        playDefault:function(){
            var item = this.episodes.at(0);
            this.playEpisode(item.id);
        },
        playEpisode:function(id){
            var item = this.episodes.get(id);
            if(item.get('media'))
                this.playMedia(item);
        },
        playMedia:function(item){
            var media_ref = item.get('media');
            var media = this.medias.findWhere({resource_uri:media_ref});
            this.components.player.view.once(
                'player:ready',
                this.components.player.view.play, 
                this.components.player.view
            );
            this.components.player.view.loadMedia(media);
            
            item.set({
                visited:true,
                current:true,
            });
            if(this.current_episode !== undefined)
            {
                this.current_episode.set({
                    current:false,
                });
            }
            this.current_episode = item;
        },
        saveMessage:function(subject, body){
            this.messages.create({
                subject:subject,
                body:body,
                user:ATW.Config.user_pk,
            });
        },
    });
    
    window.ATW.AppView =  AppView;
})();


