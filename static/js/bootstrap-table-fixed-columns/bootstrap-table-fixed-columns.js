(function ($) {
    'use strict';

    $.extend($.fn.bootstrapTable.defaults, {
        leftFixedColumns: true,
        leftFixedNumber: 3,
        rightFixedColumns: true,
        rightFixedNumber: 3
    });

    var BootstrapTable = $.fn.bootstrapTable.Constructor,
        _initHeader = BootstrapTable.prototype.initHeader,
        _initBody = BootstrapTable.prototype.initBody,
        _resetView = BootstrapTable.prototype.resetView;

    BootstrapTable.prototype.initFixedColumns = function () {
        this.timeoutHeaderColumns_ = 0;
        this.timeoutBodyColumns_ = 0;
        if (this.options.leftFixedColumns) {
            this.$fixedHeader = $([
            '<div class="fixed-table-header-columns"style=border-right:1px solid #ccc;">',
            '<table>',
            '<thead></thead>',
            '</table>',
            '</div>'].join(''));

            this.$fixedHeader.find('table').attr('class', this.$el.attr('class'));
            this.$fixedHeaderColumns = this.$fixedHeader.find('thead');
            this.$tableHeader.before(this.$fixedHeader);

            this.$fixedBody = $([
                '<div class="fixed-table-body-columns  left-body-columns">',
                '<table>',
                '<tbody></tbody>',
                '</table>',
                '</div>'].join(''));

            this.$fixedBody.find('table').attr('class', this.$el.attr('class'));
            this.$fixedBodyColumns = this.$fixedBody.find('tbody');
            this.$tableBody.before(this.$fixedBody);
            //this.$fixedBody = $([
            //    '<div class="fixed-table-column" style="position: absolute; background-color: #fff; border-right:1px solid #ddd;z-index:100;">',
            //    '<table>',
            //    '<thead></thead>',
            //    '<tbody></tbody>',
            //    '</table>',
            //    '</div>'].join(''));


            //this.$fixedBody.find('table').attr('class', this.$el.attr('class'));
            //this.$fixedHeaderColumns = this.$fixedBody.find('thead');
            //this.$fixedBodyColumns = this.$fixedBody.find('tbody');
            //this.$tableBody.before(this.$fixedBody);
        }
        if (this.options.rightFixedColumns) {
            this.$rightfixedHeader = $([
            '<div class="fixed-table-header-columns right-header-columns" style="right:14px;z-index:100;background:#fff;border-left:1px solid #ccc;">',
            '<table>',
            '<thead></thead>',
            '</table>',
            '</div>'].join(''));

            this.$rightfixedHeader.find('table').attr('class', this.$el.attr('class'));
            this.$rightfixedHeaderColumns = this.$rightfixedHeader.find('thead');
            this.$tableHeader.before(this.$rightfixedHeader);

            this.$rightfixedBody = $([
                '<div class="fixed-table-body-columns right-body-columns" style="right:14px;z-index:100;background:#fff;border-left:1px solid #ccc;">',
                '<table>',
                '<tbody></tbody>',
                '</table>',
                '</div>'].join(''));

            this.$rightfixedBody.find('table').attr('class', this.$el.attr('class'));
            this.$rightfixedBodyColumns = this.$rightfixedBody.find('tbody');
            this.$tableBody.before(this.$rightfixedBody);

            //this.$rightfixedBody = $([
            //    '<div class="fixed-table-column" style="position: absolute;right:14px; background-color: #fff; top:0px;border-right:1px solid #ddd;z-index:100;">',
            //    '<table>',
            //    '<thead></thead>',
            //    '<tbody></tbody>',
            //    '</table>',
            //    '</div>'].join(''));

            //this.$rightfixedBody.find('table').attr('class', this.$el.attr('class')).css('position', 'relative').css('border', '1px solid #ddd');
            //this.$rightfixedHeaderColumns = this.$rightfixedBody.find('thead');
            //this.$rightfixedBodyColumns = this.$rightfixedBody.find('tbody');
            //this.$tableBody.before(this.$rightfixedBody);
        }
    };

    BootstrapTable.prototype.initHeader = function () {
        _initHeader.apply(this, Array.prototype.slice.apply(arguments));

        if (!this.options.leftFixedColumns && !this.options.rightFixedColumns) {
            return;
        }
        this.initFixedColumns();

        var $tr = this.$header.find('tr:eq(0)').clone(),
            $ths = $tr.clone().find('th');

        //$tr.html('');
        //左边列冻结
        if (this.options.leftFixedColumns) {
            var $newtr = $('<tr></tr>');
            $newtr.attr('data-index', $tr.attr('data-index'));
            $newtr.attr('data-uniqueid', $tr.attr('data-uniqueid'));
            debugger;
            for (var i = 0; i < this.options.leftFixedNumber; i++) {
                $newtr.append($ths.eq(i).clone());
            }
            this.$fixedHeaderColumns.html('').append($newtr);
        }
        //$tr.html('');
        //右边列冻结
        if (this.options.rightFixedColumns) {
            debugger;
            var $newtr2 = $('<tr></tr>');
            $newtr2.attr('data-index', $tr.attr('data-index'));
            $newtr2.attr('data-uniqueid', $tr.attr('data-uniqueid'));
            for (var i = 0; i < this.options.rightFixedNumber; i++) {
                $newtr2.append($ths.eq($ths.length - this.options.rightFixedNumber + i).clone());
            }
            this.$rightfixedHeaderColumns.html('').append($newtr2);
        }
    };

    BootstrapTable.prototype.initBody = function () {
        _initBody.apply(this, Array.prototype.slice.apply(arguments));

        if (!this.options.leftFixedColumns && !this.options.rightFixedColumns) {
            return;
        }

        var that = this;
        if (this.options.leftFixedColumns) {
            this.$fixedBodyColumns.html('');
            this.$body.find('> tr[data-index]').each(function () {
                var $tr = $(this).clone(),
                    $tds = $tr.clone().find('td');

                $tr.html('');
                for (var i = 0; i < that.options.leftFixedNumber; i++) {
                    $tr.append($tds.eq(i).clone());
                }
                that.$fixedBodyColumns.append($tr);
            });
        }
        if (this.options.rightFixedColumns) {
            this.$rightfixedBodyColumns.html('');
            this.$body.find('> tr[data-index]').each(function () {
                var $tr = $(this).clone(),
                    $tds = $tr.clone().find('td');

                $tr.html('');
                for (var i = 0; i < that.options.rightFixedNumber; i++) {
                    var indexTd = $tds.length - that.options.rightFixedNumber + i;
                    var oldTd = $tds.eq(indexTd);
                    var fixTd = oldTd.clone();
                    var buttons = fixTd.find('button');
                    //事件转移：冻结列里面的事件转移到实际按钮的事件
                    buttons.each(function (key, item) {
                        $(item).click(function () {
                            that.$body.find("tr[data-index=" + $tr.attr('data-index') + "] td:eq(" + indexTd + ") button:eq(" + key + ")").click();
                        });
                    });
                    $tr.append(fixTd);
                }
                that.$rightfixedBodyColumns.append($tr);
            });
        }
    };

    BootstrapTable.prototype.resetView = function () {
        _resetView.apply(this, Array.prototype.slice.apply(arguments));

        if (!this.options.leftFixedColumns && !this.options.rightFixedColumns) {
            return;
        }

        clearTimeout(this.timeoutHeaderColumns_);
        this.timeoutHeaderColumns_ = setTimeout($.proxy(this.fitHeaderColumns, this), this.$el.is(':hidden') ? 100 : 0);

        clearTimeout(this.timeoutBodyColumns_);
        this.timeoutBodyColumns_ = setTimeout($.proxy(this.fitBodyColumns, this), this.$el.is(':hidden') ? 100 : 0);
    };

    BootstrapTable.prototype.fitHeaderColumns = function () {
        var that = this,
            visibleFields = this.getVisibleFields(),
            headerWidth = 0;
        if (that.options.leftFixedColumns) {
            this.$body.find('tr:first-child:not(.no-records-found) > *').each(function (i) {
                var $this = $(this),
                    index = i;

                if (i >= that.options.leftFixedNumber) {
                    return false;
                }

                if (that.options.detailView && !that.options.cardView) {
                    index = i - 1;
                }

                that.$fixedHeader.find('thead th[data-field="' + visibleFields[index] + '"]')
                    .find('.fht-cell').width($this.innerWidth() - 1);
                headerWidth += $this.outerWidth();
            });
            this.$fixedHeader.width(headerWidth - 1).show();
        }
        if (that.options.rightFixedColumns) {
            this.$body.find('tr:first-child:not(.no-records-found) > *').each(function (i) {
                var $this = $(this),
                    index = i;

                if (i >= visibleFields.length - that.options.rightFixedNumber) {
                    //return false;


                    //if (that.options.detailView && !that.options.cardView) {
                    //    index = i - 1;
                    //}
                    debugger;
                    that.$rightfixedHeader.find('thead th[data-field="' + visibleFields[index] + '"]')
                        .find('.fht-cell').width($this.innerWidth());
                    headerWidth += $this.outerWidth();
                }
            });
            debugger;
            this.$rightfixedHeader.width(headerWidth - 1).show();
        }
    };

    BootstrapTable.prototype.fitBodyColumns = function () {
        var that = this,
            top = -(parseInt(this.$el.css('margin-top')) - 2),
            height = this.$tableBody.height() - 2;

        if (that.options.leftFixedColumns) {
            if (!this.$body.find('> tr[data-index]').length) {
                this.$fixedBody.hide();
                return;
            }
            if (!this.options.height) {
                top = this.$fixedHeader.height() - 1;
                height = height - top;
            }

            this.$fixedBody.css({
                width: this.$fixedHeader.width(),
                height: height - 13,
                top: top + 1
            }).show();


            this.$body.find('> tr').each(function (i) {
                that.$fixedBody.find('tbody tr:eq(' + i + ')').height($(this).height());
            });

            //// events
            this.$tableBody.on('scroll', function () {
                that.$fixedBody.find('table').css('top', -$(this).scrollTop());
            });
            this.$body.find('> tr[data-index]').off('hover').hover(function () {
                var index = $(this).data('index');
                that.$fixedBody.find('tr[data-index="' + index + '"]').addClass('hover');
            }, function () {
                var index = $(this).data('index');
                that.$fixedBody.find('tr[data-index="' + index + '"]').removeClass('hover');
            });
            this.$fixedBody.find('tr[data-index]').off('hover').hover(function () {
                var index = $(this).data('index');
                that.$body.find('tr[data-index="' + index + '"]').addClass('hover');
            }, function () {
                var index = $(this).data('index');
                that.$body.find('> tr[data-index="' + index + '"]').removeClass('hover');
            });
        }
        if (that.options.rightFixedColumns) {
            if (!this.$body.find('> tr[data-index]').length) {
                this.$rightfixedBody.hide();
                return;
            }
            if (!this.options.height) {
                top = this.$rightfixedHeader.height() - 1;
                height = height - top;
            }

            this.$rightfixedBody.css({
                width: this.$rightfixedHeader.width(),
                height: height - 13,
                //top: top + 1
            }).show();


            this.$body.find('> tr').each(function (i) {
                that.$rightfixedBody.find('tbody tr:eq(' + i + ')').height($(this).height());
            });

            //// events
            this.$tableBody.on('scroll', function () {
                that.$rightfixedBody.find('table').css('top', -$(this).scrollTop());
            });
            this.$body.find('> tr[data-index]').off('hover').hover(function () {
                var index = $(this).data('index');
                that.$rightfixedBody.find('tr[data-index="' + index + '"]').addClass('hover');
            }, function () {
                var index = $(this).data('index');
                that.$rightfixedBody.find('tr[data-index="' + index + '"]').removeClass('hover');
            });
            this.$rightfixedBody.find('tr[data-index]').off('hover').hover(function () {
                var index = $(this).data('index');
                that.$body.find('tr[data-index="' + index + '"]').addClass('hover');
            }, function () {
                var index = $(this).data('index');
                that.$body.find('> tr[data-index="' + index + '"]').removeClass('hover');
            });
        }
    };

})(jQuery);