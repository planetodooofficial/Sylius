function submit_quickbook_data() {
                                $.ajax({
                                  'url': 'add_quick_b_data',
                                  'type': 'POST',
                                  'data': $('#quickbook_data').serialize(),
                                  'success': function(data) {
                                    
                                    
                                    data = JSON.parse(data);
                                    $("#loading").show();
                                    
                                    setTimeout(function() {
                                        setTimeout(function() {showSpinner();},30);
                                        window.location.replace(data['url']);
                                    },0);

                                  }
                                });
                               
                              }
                        function showSpinner() {
                            var opts = {
                              lines: 15, 
                              length: 3, 
                              width: 4, 
                              radius: 30, 
                              rotate: 0, 
                              color: '#fff', 
                              speed: 2, 
                              trail: 70, 
                              shadow: false, 
                              hwaccel: false, 
                              className: 'spinner', 
                              zIndex: 2e9, 
                              top: 'auto', 
                              left: 'auto' 
                            };
                            $('#loading_anim').each(function() {
                                spinner = new Spinner(opts).spin(this);
                            });
                        }
                        
                        function submit_import_products() {
                                 var done =0;
                                $.ajax({
                                  'url': 'add_import_products_data',
                                  'type': 'POST',
                                  'data': $('#quickbook_data').serialize(),
                                  'success': function(data) {
                                     done = 1;
                                     alert('Done!');
                                    data = JSON.parse(data);

                                    $("#loading").show();

                                    setTimeout(function() {
                                        setTimeout(function() {showSpinner();},30);
                                        window.location.replace(data['url']);
                             update_products       },0);
                                  }
                                });

                              }

                                 function import_product_variants() {
                                 var done =0;
                                $.ajax({
                                  'url': 'import_product_variants',
                                  'type': 'POST',
                                  'data': $('#quickbook_data').serialize(),
                                  'success': function(data) {
                                     done = 1;
                                     alert('Done!');
                                    data = JSON.parse(data);

                                    $("#loading").show();

                                    setTimeout(function() {
                                        setTimeout(function() {showSpinner();},30);
                                        window.location.replace(data['url']);
                             update_products       },0);
                                  }
                                });

                              }
                        function submit_import_customers(){
                                 var done =0;
                                $.ajax({
                                  'url': 'import_customer_sylius',
                                  'type': 'POST',
                                  'data': $('#quickbook_data').serialize(),
                                  'success': function(data) {
                                     done = 1;
                                     alert('Done!');
                                    data = JSON.parse(data);

                                    $("#loading").show();

                                    setTimeout(function() {
                                        setTimeout(function() {showSpinner();},30);
                                        window.location.replace(data['url']);
                                    },0);
                                  }
                                });

                              }

                        function import_country_codes(){
                                 var done =0;
                                $.ajax({
                                  'url': 'import_country_codes',
                                  'type': 'POST',
                                  'data': $('#quickbook_data').serialize(),
                                  'success': function(data) {
                                     done = 1;
                                     alert('Done!');
                                    data = JSON.parse(data);

                                    $("#loading").show();

                                    setTimeout(function() {
                                        setTimeout(function() {showSpinner();},30);
                                        window.location.replace(data['url']);
                                    },0);
                                  }
                                });

                              }

                              function submit_import_orders(){
                                 var done =0;
                                $.ajax({
                                  'url': 'import_order_sylius',
                                  'type': 'POST',
                                  'data': $('#quickbook_data').serialize(),
                                  'success': function(data) {
                                     done = 1;
                                     alert('Done!');
                                    data = JSON.parse(data);

                                    $("#loading").show();

                                    setTimeout(function() {
                                        setTimeout(function() {showSpinner();},30);
                                        window.location.replace(data['url']);
                                    },0);
                                  }
                                });

                              }
                        
                        function submit_export_products() {
                               var done =0;
                                $.ajax({
                                  'url': 'add_export_products_data',
                                  'type': 'POST',
                                  'data': $('#quickbook_data').serialize(),
                                  'success': function(data) {
                                     done =1;
                                     alert('Done!');
                                    data = JSON.parse(data);

                                    $("#loading").show();
                                    
                                    setTimeout(function() {
                                        setTimeout(function() {showSpinner();},30);
                                        window.location.replace(data['url']);
                                    },0);
                                  }
                                });

                              }
                            
                        function export_quickbook_vendor() {
                                $.ajax({
                                  'url': 'export_quick_b_vendor',
                                  'type': 'POST',
                                  'data': $('#quickbook_data').serialize(),
                                  'success': function(data) {

                                   data = JSON.parse(data);
                                   alert('Done!')
                                   $("#loading").show();
                                    
                                    setTimeout(function() {
                                        setTimeout(function() {showSpinner();},30);
                                        window.location.replace(data['url']);
                                    },0);
                                  }
                                });
                               
                              }
                            
                            function submit_update_products() {
                                $.ajax({
                                  'url': 'update_products_sylius',
                                  'type': 'POST',
                                  'data': $('#quickbook_data').serialize(),
                                  'success': function(data) {
                                      alert('Done!');
                                    data = JSON.parse(data);
                                    alert('Done!');
                                    $("#loading").show();
                                    
                                    setTimeout(function() {
                                        setTimeout(function() {showSpinner();},30);
                                        window.location.replace(data['url']);
                                    },0);
                                  }
                                });
                               
                              }
                        
                            function submit_quickbook_items() {
                                $.ajax({
                                  'url': 'add_quick_b_items',
                                  'type': 'POST',
                                  'data': $('#quickbook_data').serialize(),
                                  'success': function(data) {

                                    data = JSON.parse(data);
                                    $("#loading").show();
                                    
                                    setTimeout(function() {
                                        setTimeout(function() {showSpinner();},30);
                                        window.location.replace(data['url']);
                                    },0);
                                  }
                                });
                               
                              }
                        
                            function export_quickbook_items() {
                                $.ajax({
                                  'url': 'export_quick_b_items',
                                  'type': 'POST',
                                  'data': $('#quickbook_data').serialize(),
                                  'success': function(data) {

                                    data = JSON.parse(data);
                                    $("#loading").show();
                                    
                                    setTimeout(function() {
                                        setTimeout(function() {showSpinner();},30);
                                        window.location.replace(data['url']);
                                    },0);
                                  }
                                });
                               
                              }
                        
                        
                        
                            function submit_quickbook_invoice() {
                                $.ajax({
                                  'url': 'add_quick_b_invoice',
                                  'type': 'POST',
                                  'data': $('#quickbook_data').serialize(),
                                  'success': function(data) {

                                    data = JSON.parse(data);
                                    $("#loading").show();
                                    
                                    setTimeout(function() {
                                        setTimeout(function() {showSpinner();},30);
                                        window.location.replace(data['url']);
                                    },0);
                                  }
                                });
                               
                              }
                        
                            function export_quickbook_invoice() {
                                $.ajax({
                                  'url': 'export_quick_b_invoice',
                                  'type': 'POST',
                                  'data': $('#quickbook_data').serialize(),
                                  'success': function(data) {

                                    data = JSON.parse(data);
                                    $("#loading").show();
                                    
                                    setTimeout(function() {
                                        setTimeout(function() {showSpinner();},30);
                                        window.location.replace(data['url']);
                                    },0);
                                  }
                                });
                               
                              }
                        
                            function submit_quickbook_purchase() {
                                $.ajax({
                                  'url': 'add_quick_b_purchase',
                                  'type': 'POST',
                                  'data': $('#quickbook_data').serialize(),
                                  'success': function(data) {

                                    data = $.parseJSON(data);
                                    $("#loading").show();
                                    
                                    setTimeout(function() {
                                        setTimeout(function() {showSpinner();},30);
                                        window.location.replace(data['url']);
                                    },0);
                                  }
                                });
                               
                              }
                        
                            function export_quickbook_purchase() {
                                $.ajax({
                                  'url': 'export_quick_b_purchase',
                                  'type': 'POST',
                                  'data': $('#quickbook_data').serialize(),
                                  'success': function(data) {

                                    data = $.parseJSON(data);
                                    $("#loading").show();
                                    
                                    setTimeout(function() {
                                        setTimeout(function() {showSpinner();},30);
                                        window.location.replace(data['url']);
                                    },0);
                                  }
                                });
                               
                              }
                        
                            function submit_quickbook_sale() {
                                $.ajax({
                                  'url': 'add_quick_b_sale',
                                  'type': 'POST',
                                  'data': $('#quickbook_data').serialize(),
                                  'success': function(data) {

                                    data = $.parseJSON(data);
                                    $("#loading").show();
                                    
                                    setTimeout(function() {
                                        setTimeout(function() {showSpinner();},30);
                                        window.location.replace(data['url']);
                                    },0);
                                  }
                                });
                               
                              }
                            function export_quickbook_sale() {
                                $.ajax({
                                  'url': 'export_quick_b_sale',
                                  'type': 'POST',
                                  'data': $('#quickbook_data').serialize(),
                                  'success': function(data) {

                                    data = $.parseJSON(data);
                                    $("#loading").show();
                                    
                                    setTimeout(function() {
                                        setTimeout(function() {showSpinner();},30);
                                        window.location.replace(data['url']);
                                    },0);
                                  }
                                });
                               
                              }
                        