using Gee;

namespace Stegosaurus {
  public class RandomCursor : GLib.Object {
    private Iterator<int> valuesIterator;

    public RandomCursor(int seed, int start, int end) {
      GLib.Random.set_seed(seed);
      var values = new ArrayList<int> ();
      while (values.size < end-start) {
        int number = GLib.Random.int_range(start, end);
        if (values.contains(number)){
            continue;
        }
        values.add(number);
      }
      this.valuesIterator = values.iterator();
    }
    public bool next(out int result) {
      if (this.valuesIterator.next()){
          result = this.valuesIterator.get();
          return true;
      }
      return false;
    } 
  }
  public class Random : GLib.Object {
    public Random() {
      
    }
    public RandomCursor rand_int(int seed, int start, int end){
      return new RandomCursor(seed, start, end);
    }
  }
  static int main (string[] args){
    Random rand = new Random();
    RandomCursor randCursor = rand.rand_int(0, 0, 10);
    int res;
    while (randCursor.next(out res)){
      stdout.printf("%d\n", res);
    }
    return 0;
  }
}