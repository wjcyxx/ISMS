/**
 * @author: Dennis Hernández
 * @webSite: http://djhvscf.github.io/Blog
 * @version: v1.0.0
 */

(function ($) {
    'use strict';
	var table1,tablew=0,afterScroll=true,n = 1;//tablew记录上一次的table宽度；afterScroll记录上一次的table是否有滚动条
    var initResizable = function (that) {
        //Deletes the plugin to re-create it
    	
        table1 = that.$el.parents('.fixed-table-container').find('table').eq(0);
    	if(table1.find('th').size()==0){
    		table1 = that.$el;
    	}
        table1.colResizable({disable: true});

        //Creates the plugin
        table1.colResizable({
            liveDrag: that.options.liveDrag,
            fixed: that.options.fixed,
            headerOnly: that.options.headerOnly,
            minWidth: that.options.minWidth,
            hoverCursor: that.options.hoverCursor,
            dragCursor: that.options.dragCursor,
            onResize: that.onResize,
            onDrag: that.options.onResizableDrag
        });
		if(n==1){
			tablew = that.$el.width();n++;
		}
		
    };

    $.extend($.fn.bootstrapTable.defaults, {
        resizable: false,
        liveDrag: false,
        fixed: true,
        headerOnly: false,
        minWidth: 15,
        hoverCursor: 'e-resize',
        dragCursor: 'e-resize',
        onResizableResize: function (e) {
            return false;
        },
        onResizableDrag: function (e) {
            return false;
        }
    });

    var BootstrapTable = $.fn.bootstrapTable.Constructor,
        _toggleView = BootstrapTable.prototype.toggleView,
        _resetView = BootstrapTable.prototype.resetView,
        _resetWidth = BootstrapTable.prototype.resetWidth;
        

    BootstrapTable.prototype.toggleView = function () {
        _toggleView.apply(this, Array.prototype.slice.apply(arguments));

        if (this.options.resizable && this.options.cardView) {
            //Deletes the plugin
            $(this.$el).colResizable({disable: true});
        }
    };
var t;
    BootstrapTable.prototype.resetView = function () {
        var that = this;
        _resetView.apply(this, Array.prototype.slice.apply(arguments));

        if (this.options.resizable) {
            // because in fitHeader function, we use setTimeout(func, 100);
            clearTimeout(t);
            t = setTimeout(function () {
                initResizable(that);
            }, 100);
        }
    };
    BootstrapTable.prototype.resetWidth = function () {
        var that = this;
        _resetWidth.apply(this, Array.prototype.slice.apply(arguments));

        if (this.options.resizable) {
            // because in fitHeader function, we use setTimeout(func, 100);
            clearTimeout(t);
            t = setTimeout(function () {
                initResizable(that);
            }, 100);
        }
    };

    BootstrapTable.prototype.onResize = function (e,nn) {
    	var ths = table1.find('thead>tr>th');
    	var that = table1.parents('.fixed-table-container').find('table').eq(1);
    	table1.parents('.fixed-table-container').height()<that.height()?afterScroll==true:afterScroll==false;
    	
    	ths.each(function(index){
    		var h = $(this)[0].style.width;
    		var w0 =  that.width()-tablew;
			$(this).find('.fht-cell').width(h);
			that.find('thead th').eq(index).width(h);
			that.find('.fht-cell').eq(index).width(h);
    	})
if(!nn){
	that.data('bootstrap.table').options.onResizableResize.apply(e);
	
}
		that.bootstrapTable('resetWidth');
    }
})(jQuery);
