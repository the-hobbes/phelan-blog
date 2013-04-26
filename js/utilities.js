var BROWSER = {
	w				: window.innerWidth,
	h				: window.innerHeight,
	test_touchable : function(){
		var result;
		try { document.createEvent('TouchEvent'); } catch(e){ result = e; }
		if(result){
			return false;
		} else {
			return true;
		}
	},
};
BROWSER.touchable = BROWSER.test_touchable();

function random_from_to(from, to){
	return Math.floor(Math.random() * (to - from + 1) + from);
}