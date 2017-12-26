import Control.Monad.State
type Stat = (Int,Integer,Integer)


eul :: Int -> Double -> Double -> Double
eul 0 y0 dx = y0
eul n y0 dx = y1 + (f' y1) * dx
  where
    y1  = eul (n-1) y0 dx
    f' y = y

    -- fib_ :: Int -> Int
    -- fib_ 0 = 0
    -- fib_ 1 = 1
    -- fib_ n = fib_ (n-1) + fib_ (n-2)
-- fib :: Int -> Integer
-- fib 0 = 0
-- fib 1 = 1
-- fib n = evalState fibImpl (2, 1, 0)
--   where
--     fibImpl :: State Stat Integer
--     fibImpl = do
--       (i, r1, r2) <- get
--       if i == n
--         then return $ r1 + r2
--         else do
--           put (i + 1, r1 + r2, r1)
--           fibImpl

main :: IO()
main = do
  let xrange = (0,1)
  let n_max  =  100 :: Int
  let init_y =  1.0
  let dx = (snd xrange - fst xrange) / fromIntegral n_max
  print $eul n_max init_y dx
