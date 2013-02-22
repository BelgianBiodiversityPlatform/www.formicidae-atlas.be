// We avoid polluting the global namespace:
// http://marcofranssen.azurewebsites.net/writing-modular-javascript-without-polluting-the-global-namespace/

; (function($, formidabel, window, document, undefined) {
	// Atlas follows the Module pattern
    var atlas = formidabel.atlas = formidabel.atlas || (function(){
        var squares;

        var SQUARE_PROVIDER = (function(){
            var squares;

            var loadSquaresData = function (squares_source_url) {
                var json = null;
                $.ajax({ 'async': false, 'global': false, 'url': squares_source_url,
                'dataType': "json",
                'success': function (data) {
                    json = data;
                    }
                });
                return json;
            };

            var initialize = function(squares_source_url){
                squares = loadSquaresData(squares_source_url);
            };

            var getSquare = function(square_id){
                // Returns GeoJSON object corresponding to the Square ID, or undefined.
                var square = _.find(squares.features, function(sq){
                    return sq.properties.TAG == square_id;
                });
                return square;
            };

            return {
                'initialize': initialize,
                'getSquare': getSquare
            };


        })();
        
        var Occurrence = Backbone.Model.extend({
            addToMap: function(){
                console.log("Ajout occurrence");
                console.log(this.attributes);
            }
        });

        var OccurrenceList = Backbone.Collection.extend({
			model: Occurrence,

            // Store the species_id, so it will be available to build retrieval URL
            initialize: function(species_id){
                this.species_id = species_id;
            },

            url: function(){
                return '/api/v1/species/' + this.species_id;
            },

            // The server "to be stored" data is returned in the occurrences attribute
            // That's what we should use to build each Occurrence
            parse: function(response){
                return response.occurrences;
            }
        });
        
        var OccurrenceSearch = Backbone.Model.extend({
            // Fill the data from server
            // Should we overrive fetch instead ?
            loadOccurrences: function(){
                col = new OccurrenceList(this.get('species_id'));
                this.set('collection', col); // We'll now have a collection attribute
                
                var that = this;
                col.fetch({success: function(){
                    // Once its loaded, render that !
                    v = new OccurrenceSearchView({model: that});
                    v.render();
                }});
            }
        });

        // Should receive a OccurrenceSearch as model argument
        var OccurrenceSearchView = Backbone.View.extend({
            el: $('#search_list'), // TODO: decouple

            render: function(){
                var m = this.model;

                // Add to search list
                $(this.el).append('<p>Recherche species ' + m.get('species_id') + '</p>');
                // Ask each occurrence to render itself
                m.get('collection').each(function(occ){
                    occ.addToMap();
                });

            }
        });

        var SearchView = Backbone.View.extend({
            events: {
                'submit #search': 'trigger_search'
            },

            trigger_search: function(){
                var s = new OccurrenceSearch({
                    species_id: this.$('#species_id').val(),
                    color: '#ab13cc' // Make color configurable
                });

                s.loadOccurrences();

                return false; // Don't submit the search form
            }
        });

        var mapInit = function(map_options){
            // Todo: make dom element configurable
            var map = L.map('map').setView(map_options.initial_location, map_options.initial_zoom);

            L.tileLayer('http://{s}.tile.cloudmade.com/' + map_options.cloudmade_api_key + '/' + map_options.cloudmade_style_id + '/256/{z}/{x}/{y}.png', {
                attribution: map_options.attribution,
                maxZoom: map_options.max_zoom
            }).addTo(map);
        };


        // TODO: Move loadSquaresData(), getSquare() and the squares variable to a specific (squaresProvider?) module.
        

        /**/

        var bootstrap = function(app_container, map_options, app_options){
            // Main view that observes the search form
            SQUARE_PROVIDER.initialize(app_options.squares_source_url);

            mapInit(map_options);

            var f = new SearchView({el: app_container});
        };

        // Export public members
        return {
			bootstrap: bootstrap,
            sq: SQUARE_PROVIDER.getSquare
        };

    }());
}(jQuery, window._formidabel = window._formidabel || {}, window, document));