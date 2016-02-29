/* ==========================================================================
   Scripts for `/sub-pages/*`.
   ========================================================================== */

'use strict';

var SecondaryNavigation = require( '../../organisms/SecondaryNavigation' );
var sidebarDom = document.querySelector( '.content_sidebar' );
var secondaryNavigation = new SecondaryNavigation( sidebarDom ).init();
