/**
 * Check if an element exists on the page, and if it does, add listeners.
 * @param {NodeList} elems - A list of elements.
 * @param {string} event - An event string, probably a "MouseEvent."
 * @param {Function} callback - The event handler.
 */
function addEventListenerToElems( elems, event, callback ) {
  let elem;
  for ( const i in elems ) {
    elem = elems[i];
    if ( elem.addEventListener ) {
      addEventListenerToElem( elems[i], event, callback );
    }
  }
}

/**
 * Check if an element exists on the page, and if it does, add listeners.
 * @param {[type]}   elem     [description]
 * @param {[type]}   event    [description]
 * @param {Function} callback [description]
 */
function addEventListenerToElem( elem, event, callback ) {
  if ( elem ) {
    elem.addEventListener( event, callback );
  } else {
    analyticsLog( `${ elem } doesn't exist!` );
  }
}

/**
 * Log a message to the console if the `debug-gtm` URL parameter is set.
 * @param {string} msg - Message to load to the console.
 */
function analyticsLog( ...msg ) {
  if ( getQueryParameter( 'debug-gtm' ) === true ) {
    console.log( `ANALYTICS DEBUG MODE: ${ msg }` );
  }
}

/* Search for support of the matches() method by looking at
   browser prefixes.
   @param {HTMLNode} elem
   The element to check for support of matches() method.
   @returns {Function} The appropriate matches() method of elem. */
function _getMatchesMethod( elem ) {
  return elem.matches ||
       elem.webkitMatchesSelector ||
       elem.mozMatchesSelector ||
       elem.msMatchesSelector;
}

/**
 * Get the nearest parent node of an element.
 *
 * @param {HTMLNode} elem - A DOM element.
 * @param {string} selector - CSS selector.
 * @returns {HTMLNode} Nearest parent node that matches the selector.
 */
function closest( elem, selector ) {
  elem = elem.parentNode;

  const matchesSelector = _getMatchesMethod( elem );
  let match;

  while ( elem ) {
    if ( matchesSelector.bind( elem )( selector ) ) {
      match = elem;
    } else {
      elem = elem.parentElement;
    }

    if ( match ) { return elem; }
  }

  return null;
}

function Delay() {
  let timer = 0;
  return function( callback, ms ) {
    clearTimeout( timer );
    timer = setTimeout( callback, ms );
  };
}

/**
 * TODO: Merge with Analytics.js.
 * Track an analytics event and log the event.
 * @param {string} event Type of event.
 * @param {string} action Name of event.
 * @param {string} label DOM element label.
 */
function track( event, action, label ) {
  window.dataLayer.push( {
    event: event,
    action: action,
    label: label
  } );
  analyticsLog( event, action, label );
}

/**
 * Check if two hosts are the same.
 * This only works with a www subdomain.
 * @param {string} host1 - A URL.
 * @param {string} host2 - Another URL.
 * @returns {boolean} True if the hosts are equal, false otherwise.
 */
function hostsAreEqual( host1, host2 ) {

  /**
   * Pick the host out of a URL.
   * @param {string} srcHost - A URL
   * @returns {string} A hostname without subdomain.
   */
  function createTestHost( srcHost ) {
    let testHost = document.createElement( 'a' );
    testHost.href = srcHost;

    testHost = testHost.host;
    if ( testHost.substring( 0, 4 ) === 'www.' ) {
      testHost = testHost.substring( 4 );
    }

    return testHost;
  }

  return createTestHost( host1 ) === createTestHost( host2 );
}

/**
 * Retrieve a URL query string parameter by parameter name.
 * @param  {string} key - The name of the parameter in the URL.
 * @returns {string|null} The value of the parameter.
 */
function getQueryParameter( key ) {
  const url = window.location.href;
  const param = key.replace( /[\[\]]/g, '\\$&' );
  const regex = new RegExp( '[?&]' + param + '(=([^&#]*)|&|#|$)' );
  const results = regex.exec( url );
  if ( !results ) return null;
  if ( !results[2] ) return '';
  const decoded = decodeURIComponent( results[2].replace( /\+/g, ' ' ) );
  if ( decoded === 'true' ) return true;
  if ( decoded === 'false' ) return false;
  return decoded;
}

module.exports = {
  addEventListenerToElems,
  addEventListenerToElem,
  analyticsLog,
  closest,
  Delay,
  getQueryParameter,
  hostsAreEqual,
  track
};
