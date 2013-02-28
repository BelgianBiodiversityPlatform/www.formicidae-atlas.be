// We avoid polluting the global namespace:
// http://marcofranssen.azurewebsites.net/writing-modular-javascript-without-polluting-the-global-namespace/

; (function($, formidabel, window, document, undefined) {
	// Atlas follows the Module pattern
    var atlas = formidabel.atlas = formidabel.atlas || (function(){
        var map;
        var layerControl;

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
                // Returns GeoJSON object corresponding to the Square ID, or undefined if square is not found.
            
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
            events: {
                'click .remove': 'myremove'
            },

            render: function(){
                var layerStyle;
                var squaresToDisplay;
                var found;

                var m = this.model;

                // 1. Add to search list
                m.layer_list_entry = $('<p>Species ' + m.get('species_id') + ' <span class="remove">Remove</span>'+ '</p>');
                $(this.el).html(m.layer_list_entry);
                $('#search_list').append(this.$el); // TODO: decouple

                // 2. Add to map
                squaresToDisplay = [];
                
                // 2.1 Fill squaresToDisplay with square label and # of occurrences
                m.get('collection').each(function(occ){
                    found = false;
                    _.each(squaresToDisplay, function(sq){
                        // If object already exists, increment counter
                        if (sq.label === occ.attributes.square.label) {
                            sq.counter += 1;
                            found = true;
                        }
                    });
                    if (found === false){
                        // Else, add a new one
                        squaresToDisplay.push({
                            label: occ.attributes.square.label,
                            counter: 1
                        });
                    }
                });

                // 2.2 Create layer...
                layerStyle = function(feature){
                    return {
                        color: m.get('color'),
                        fillOpacity: feature.properties.occurrence_counter / 5.0
                    };
                };

                m.layer = L.geoJson([], {style: layerStyle}).addTo(map);
                layerControl.addOverlay(m.layer, 'Species ' + m.get('species_id'));
                
                // 2.3 and fill it
                _.each(squaresToDisplay, function(s){
                    var square_data = SQUARE_PROVIDER.getSquare(s.label);
                    if (square_data !== undefined){
                        square_data.properties.occurrence_counter = s.counter;
                        m.layer.addData(square_data);
                    }
                });
                
            },

            myremove: function(){
                map.removeLayer(this.model.layer); // Do our specific stuff...
                this.remove(); // Then call backbone's remove() to kill el
            }
            
        });

        var SearchView = Backbone.View.extend({
            events: {
                'submit #search': 'trigger_search'
            },

            trigger_search: function(){
                var s = new OccurrenceSearch({
                    species_id: this.$('#species_id').val(),
                    color: this.$('#color_code').val() // TODO: Make color configurable
                });

                s.loadOccurrences();

                return false; // Don't submit the search form
            }
        });

        var mapInit = function(map_options){
            // Todo: make dom element configurable
            var cloudmade, google;
            var baseLayers;

            map = L.map('map').setView(map_options.initial_location, map_options.initial_zoom);

            cloudmade = L.tileLayer('http://{s}.tile.cloudmade.com/' + map_options.cloudmade_api_key + '/' + map_options.cloudmade_style_id + '/256/{z}/{x}/{y}.png', {
                attribution: map_options.attribution,
                maxZoom: map_options.max_zoom
            }).addTo(map);

            google = new L.Google();

            baseLayers = {
                "CloudMade": cloudmade,
                "Google": google
            };

            layerControl = L.control.layers(baseLayers, {}).addTo(map);
        };

        var bootstrap = function(app_container, map_options, app_options){
            SQUARE_PROVIDER.initialize(app_options.squares_source_url);
            mapInit(map_options);
            var f = new SearchView({el: app_container}); // Main view that observes the search form
        };

        // Export public members
        return {
			bootstrap: bootstrap
        };

    }());
}(jQuery, window._formidabel = window._formidabel || {}, window, document));