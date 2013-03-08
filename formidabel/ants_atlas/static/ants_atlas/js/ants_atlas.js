// We avoid polluting the global namespace:
// http://marcofranssen.azurewebsites.net/writing-modular-javascript-without-polluting-the-global-namespace/

; (function($, formidabel, window, document, undefined) {
	// Atlas follows the Module pattern
    var atlas = formidabel.atlas = formidabel.atlas || (function(){
        var map;
        var layerControl;

        var spinner_layer;

        var config; // Contains config passed in app_options

        var utils = {
            formFieldToDate: function(elem){
                // Returns a Date object or null
                var min_date = $(elem).val();
                if (min_date === ""){
                    return null;
                } else {
                    return new Date(min_date);
                }
            }
        };

        // TODO: Make a module with the next 3 declarations
        var overlayColorPresets; // List of colors
        var overlayColorPresets_index=0; // Pointer to this list
        var nextColorPresetInSearchForm = function(force){
            // Fill the color field from the form. Will only work if the field is empty or if force is true
            var new_value;
            var $elem = $('#color_code');

            if (force === true || $elem.val() === ''){
                new_value = overlayColorPresets[overlayColorPresets_index];

                $elem.val(new_value);
                overlayColorPresets_index++;
                if (overlayColorPresets_index === overlayColorPresets.length){
                    // Cycle on the array
                    overlayColorPresets_index = 0;
                }

            }

        };

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
                return config.species_api_url + this.species_id;
            },

            // The server "to be stored" data is returned in the occurrences attribute
            // That's what we should use to build each Occurrence
            parse: function(response){
                return response.occurrences;
            },

            my_filter: function(filters){
                var results = this;


                if (filters.min_date) {
                    results = new OccurrenceList(results.filter(function(o){
                        return new Date(o.attributes.event_date) >= filters.min_date;
                        }));
                    }
                if (filters.max_date) {
                    //console.log("passe max date");
                    results = new OccurrenceList(results.filter(function(o){
                        return new Date(o.attributes.event_date) <= filters.max_date;
                        }));
                    }    

                return results;
            }
        });

        var OccurrenceSearch = Backbone.Model.extend({
            // Fill the data from server
            // Should we overrive fetch instead ?
            loadOccurrences: function(){
                col = new OccurrenceList(this.get('species_id'));
                this.set('collection', col); // We'll now have a collection attribute

                var that = this;

                spinner_layer.fire('data:loading');

                col.fetch({success: function(){
                    var filtered;

                    // if (that.get('filters').min_date){
                    //     that.set('collection', col.my_filter({min_date: that.get('filters').min_date}));
                    // }

                    if (that.get('filters').min_date || that.get('filters').max_date){
                        that.set('collection', col.my_filter(that.get('filters')));
                    }

                    // Once its loaded, render that !
                    v = new OccurrenceSearchView({model: that});
                    v.render();
                    spinner_layer.fire('data:loaded');
                }});
            }
        });

        // Should receive a OccurrenceSearch as model argument
        var OccurrenceSearchView = Backbone.View.extend({
            template: _.template($("#layerListEntry").html()),
            tagName: 'tr',

            events: {
                'click .remove': 'myremove'
            },

            render: function(){
                var layerStyle;
                var squaresToDisplay;
                var found;
                var template;

                var m = this.model;

                var species_name = m.get('species_name');
                var occurrences = m.get('collection');

                // 1. Add to search list
                $(this.el).html(this.template({
                    species_name: species_name,
                    occurrences_count: _.size(occurrences)
                }));
                $('#search_list').append(this.$el); // TODO: decouple

                // 2. Add to map
                squaresToDisplay = [];

                // 2.1 Fill squaresToDisplay with square label and # of occurrences
                occurrences.each(function(occ){
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

                // 2.2 Create layer w/ style & popup
                m.layer = L.geoJson([], {
                    style: function(feature){
                        return {
                            weight: 2,
                            color: m.get('color'),
                            fillOpacity: feature.properties.occurrence_counter / 5.0
                        };
                    },

                    onEachFeature: function(feature, layer){
                        var p = feature.properties;

                        layer.bindPopup(_.template($("#mapPopupContent").html(), {
                            occ_counter: p.occurrence_counter,
                            square_id: p.TAG,
                            species_name: species_name
                        }));
                    }
                }).addTo(map);

                layerControl.addOverlay(m.layer, species_name);

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
                layerControl.removeLayer    (this.model.layer);
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
                    filters: {
                        'min_date': utils.formFieldToDate(this.$('#min_date')),
                        'max_date': utils.formFieldToDate(this.$('#max_date'))
                    },

                    species_id: this.$('#species_id').val(),
                    species_name: this.$("#species_id option:selected").text(),
                    color: this.$('#color_code').val()
                });

                s.loadOccurrences();

                // Propose a new color preset for next search
                nextColorPresetInSearchForm(true);

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
                "Google satellite": google
            };

            spinner_layer = L.geoJson(null).addTo(map);

            // TODO: Make it configurable
            var phytonregions = L.tileLayer.wms("http://gis.bebif.be:80/geoserver2/wms", {
                layers: 'bbpf:Regions_Phyto_Clipped',
                format: 'image/png',
                transparent: true
            });

            layerControl = L.control.layers(baseLayers, {'phytonregions': phytonregions}).addTo(map);

            overlayColorPresets = map_options.overlay_color_presets; // Store for future use
        };

        var bootstrap = function(app_container, map_options, app_options){
            // Keep configuration for future use
            config = app_options;

            SQUARE_PROVIDER.initialize(config.squares_source_url);
            mapInit(map_options);
            // propose a first color preset
            nextColorPresetInSearchForm();

            var f = new SearchView({el: app_container}); // Main view that observes the search form
        };

        // Export public members
        return {
			bootstrap: bootstrap
        };

    }());
}(jQuery, window._formidabel = window._formidabel || {}, window, document));