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
            this.cache = {};
            this.images.on('add', this.renderOne, this);
            this.images.on('reset', this.render, this);
        },
        initBack:function(item){
            this.$el.backstretch(item.get('image'), {fade:item.get('fade', 1000)});
            this.backstretch = this.$el.data('backstretch');
        },
        cacheImage:function(item){
            if(this.cache[item.id] !== undefined)
            {
                return;
            }
            var src = item.get('image');
            var img = new Image;
            img.src = src;
            this.cache[item.id] = img;
            $(img).on('load',function(){
                console.log('L: '+src);
            });
        },
        renderOne:function(item){
            this.cacheImage(item);
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
                
                this.registerComponent('home', new HomeView);
                this.registerComponent('episodes', new EpisodeCollectionView);
                this.registerComponent('login', new ATW.LogWidget);
                this.registerComponent('register', new ATW.RegisterWidget);
                this.registerComponent('player', new ATW.VideoPlayer);
                this.registerComponent('contact', new ATW.ContactWidget);
                
                this.components.home.view.images.fetch();
                this.components.episodes.view.episodes.fetch();
                this.episodes = this.components.episodes.view.episodes;
                
                this.messages = new ATW.Collections.message;
                
                this.trigger('ready');
            }, this);
        },
        registerComponent: function(name, view){
            if(this.components === undefined)
            {
                this.components = {};
            }
            this.components[name] = {
                view:view,
                visible:false,
                rendered: false,
            }
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


