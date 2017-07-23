import Data.List as L

main :: IO()　--メイン関数
main = do
  print $64 * tornament (1/4) 2 2 -- = 12/64 = 3/16

tornament :: Double -> Int -> Int -> Double
tornament q rank weak = average $map (tor rank) $permutations $ (take weak $repeat 0)++(take (2^rank - weak) $repeat 1)
  where average :: (Fractional a) => [a] -> a
        average xs = sum xs / fromIntegral (length xs)        

        tor :: Int -> [Int] -> Double
        tor 1 team 
                | sum team == 0 = 1
                | sum team == 1 = q
                | sum team == 2 = 0
        tor n team  = 1*q1 *q2 + q* (1-q1)*q2+ q*q1*(1-q2) + 0* (1-q1)* (1-q2)
          where 
            q1 = tor (n-1) $take (2^(n-1)) team
            q2 = tor (n-1) $drop (2^(n-1)) team