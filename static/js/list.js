function Node(v){  
    this.value=v;  
    this.next=null;  
  }  
function ArrayList(){  
     this.head=new Node(null);  
        this.tail = this.head;  
        //在尾部添加节点  
        this.append=function(v){  
          node = new Node(v);  
          this.tail.next=node;  
          this.tail=node;  
        }  
        //在指定位置插入  
        this.insertAt=function(ii,v){  
          node = new Node(v);  
          //找到位置的节点  
          tempNode=this.head;  
          for(i=0;i<ii;i++){  
            if(tempNode.next!=null){  
              tempNode=tempNode.next;  
            }else{  
              break;  
            }  
          }  
          node.next=tempNode.next;  
          tempNode.next = node;  
        }  
        //删除指定节点  
        this.removeAt=function(ii){  
          node1=this.head; //要删除节点的前一个节点  
          for(i=0;i<ii;i++){  
            if(node1.next!=null){  
              node1=node1.next;  
            }else{  
              break;  
            }  
          }  
          node2=node1.next;  //要删除的节点  
          if(node2!=null){  
            node1.next = node2.next;  
            if(node2.next==null){  
                this.tail=node1;  
              }  
          }  
        }  
        //查找值  
        this.find=function(v){  
             var nodefin=this.head;  
                while(nodefin.value!=v){  
                    if(nodefin.next!=null){  
                       nodefin=nodefin.next;  
                    }else{break;}  
                }  
                return nodefin;  
        }  
        //查找某个节点的值  
        this.findv=function(ii){  
            var nodefv = this.head;  
            for(var i =0;i<ii;i++){  
                if(nodefv.next!=null){  
                    nodefv=nodefv.next;  
                }  
            }  
            return nodefv;  
        }  
        //显示连表中的值  
        this.show=function()  
        {  
            var Node=this.head;  
            while(Node!=null)  
                {  
                  console.log(Node.value);  
                  Node=Node.next;  
                }  
        }  
}  